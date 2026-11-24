"""Trained continual-learning reference on the hard development worlds: an online neural network with experience replay.

The nearest-neighbour references (tools/reference_hard.py) store every encounter but do not learn anything. This
reference is a standard trained learner from the continual-learning literature: a small neural network that learns
online, one encounter at a time, rehearsing a replay buffer that keeps every past encounter.

Learner (one life = one world):
  - Input: the 49 published features (data/hard-dev/features_<seed>.npz), z-scored with the stream mean and standard
    deviation (+1e-6), exactly as the nearest-neighbour references; plus 4 indicators saying which senses are present.
  - Network: 53 -> H (ReLU) -> 12 colours (softmax), Adam, cross-entropy.
  - Life: for each encounter in stream order, the encounter (features + the colour seen) is added to the buffer, then
    S gradient steps are taken on minibatches of 32 drawn uniformly from the buffer, always including the newest
    encounter. Each training example gets one of the 7 test sense masks at random (all senses or one of 6 pairs);
    masked senses are set to 0 (the stream mean). Training on the test masks favours this reference.
  - End of life: every cue is answered 7 times (all senses + 6 pairs); an object is known only if all 7 are right.
    Same all-pairs measure as tools/score_hard_dev.py.

Budget, reported per life: CPU seconds (process time) and numbers held (buffer + parameters + Adam state).

Protocol: hyperparameters (H, S, learning rate) are chosen on worlds 310806-310819 only, by mean known rate over 3
training seeds; the choice is then reported on all 20 worlds and separately on 310800-310805, which were not used for
the choice. All of this is development data, not a locked exam.

Usage (repository root):
  python3 tools/reference_replay.py --grid                      # selection on 310806-310819 (about 30 minutes)
  python3 tools/reference_replay.py --H 1024 --S 4 --lr 0.003   # the chosen configuration, 20 worlds x 3 seeds
  python3 tools/reference_replay.py --H 1024 --S 16 --lr 0.003 --seeds 0   # 4x the compute, for information
"""
import argparse
import itertools
import json
import os
import pathlib
import sys
import time

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):   # small matrices: threads only slow
    os.environ.setdefault(_v, "1")                                         # it down and blur the CPU budget
import numpy as np  # noqa: E402

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "hard-dev"
BLOCKS = (("goz", 25), ("dokunma", 6), ("kulak", 8), ("koku", 10))
SELECT_WORLDS = tuple(range(310806, 310820))
CHECK_WORLDS = tuple(range(310800, 310806))
GRID = {"H": (256, 1024), "S": (1, 4), "lr": (0.003, 0.01)}
TRAIN_SEEDS = (0, 1, 2)
BATCH = 32


def masks():
    edges, i = [], 0
    for _, n in BLOCKS:
        edges.append((i, i + n))
        i += n
    out = [(np.ones(i, bool), np.ones(4))]
    for a, b in itertools.combinations(range(4), 2):
        m, ind = np.zeros(i, bool), np.zeros(4)
        for k in (a, b):
            m[edges[k][0]:edges[k][1]] = True
            ind[k] = 1.0
        out.append((m, ind))
    return out


MASKS = masks()
MASK_X = np.stack([m.astype(float) for m, _ in MASKS])   # (7, 49)
MASK_I = np.stack([ind for _, ind in MASKS])              # (7, 4)


class Net:
    def __init__(self, n_in, H, n_out, rng, lr):
        self.p = {"W1": rng.normal(0, np.sqrt(2 / n_in), (n_in, H)), "b1": np.zeros(H),
                  "W2": rng.normal(0, np.sqrt(1 / H), (H, n_out)), "b2": np.zeros(n_out)}
        self.m = {k: np.zeros_like(v) for k, v in self.p.items()}
        self.v = {k: np.zeros_like(v) for k, v in self.p.items()}
        self.t, self.lr = 0, lr

    def logits(self, X):
        h = np.maximum(X @ self.p["W1"] + self.p["b1"], 0)
        return h, h @ self.p["W2"] + self.p["b2"]

    def step(self, X, y):
        h, z = self.logits(X)
        z = z - z.max(1, keepdims=True)
        pr = np.exp(z)
        pr /= pr.sum(1, keepdims=True)
        pr[np.arange(len(y)), y] -= 1
        g2 = pr / len(y)
        gh = (g2 @ self.p["W2"].T) * (h > 0)
        grads = {"W2": h.T @ g2, "b2": g2.sum(0), "W1": X.T @ gh, "b1": gh.sum(0)}
        self.t += 1
        b1, b2 = 0.9, 0.999
        for k, g in grads.items():
            self.m[k] = b1 * self.m[k] + (1 - b1) * g
            self.v[k] = b2 * self.v[k] + (1 - b2) * g * g
            mh = self.m[k] / (1 - b1 ** self.t)
            vh = self.v[k] / (1 - b2 ** self.t)
            self.p[k] -= self.lr * mh / (np.sqrt(vh) + 1e-8)

    def numbers(self):
        return sum(v.size for v in self.p.values()) * 3   # parameters + two Adam moments


def life(seed, H, S, lr, train_seed):
    f = np.load(DATA / f"features_{seed}.npz")
    truth = np.load(DATA / f"answers_{seed}.npz")
    if not np.array_equal(f["cue_object"], truth["cue_object"]):
        raise SystemExit(f"{seed}: feature and answer files disagree on the object list")
    n_col = len(np.load(DATA / f"world_{seed}.npz")["palette"])
    t0 = time.process_time()
    X, colour = f["stream_x"], f["stream_colour"].astype(int)
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    rng = np.random.default_rng([seed, train_seed])
    net = Net(Z.shape[1] + 4, H, n_col, rng, lr)
    for t in range(len(Z)):
        for _ in range(S):
            idx = rng.integers(0, t + 1, BATCH)
            idx[0] = t
            mk = rng.integers(0, len(MASKS), BATCH)
            net.step(np.hstack([Z[idx] * MASK_X[mk], MASK_I[mk]]), colour[idx])
    C = (f["cue_x"] - mu) / sd
    ok = np.ones(len(C), bool)
    for j in range(len(MASKS)):
        _, z = net.logits(np.hstack([C * MASK_X[j], np.broadcast_to(MASK_I[j], (len(C), 4))]))
        ok &= z.argmax(1) == truth["cue_colour"]
    cpu = time.process_time() - t0
    numbers = Z.size + len(colour) + net.numbers()      # buffer (features + colour) + network and optimiser state
    return {"world": seed, "known": int(ok.sum()), "seen": int(ok.size), "cpu_s": round(cpu, 2), "numbers": numbers}


def run(H, S, lr, worlds, seeds=TRAIN_SEEDS):
    return [life(w, H, S, lr, s) | {"train_seed": s} for s in seeds for w in worlds]


def summary(rows, worlds):
    rows = [r for r in rows if r["world"] in worlds]
    seeds = sorted({r["train_seed"] for r in rows})
    per_seed = [float(np.mean([r["known"] / r["seen"] for r in rows if r["train_seed"] == s])) for s in seeds]
    k = sum(r["known"] for r in rows) / len(seeds)
    n = sum(r["seen"] for r in rows) / len(seeds)
    return {"worlds": len(worlds), "known_mean_over_seeds": k, "seen": n, "world_mean": float(np.mean(per_seed)),
            "world_mean_by_seed": [round(x, 4) for x in per_seed],
            "cpu_s_per_life_mean": round(float(np.mean([r["cpu_s"] for r in rows])), 2),
            "cpu_s_per_life_max": max(r["cpu_s"] for r in rows), "numbers": rows[0]["numbers"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--H", type=int)
    ap.add_argument("--S", type=int)
    ap.add_argument("--lr", type=float)
    ap.add_argument("--seeds", type=int, nargs="+", default=list(TRAIN_SEEDS))
    ap.add_argument("--json")
    a = ap.parse_args()
    out = {}
    if a.grid:
        for H, S, lr in itertools.product(GRID["H"], GRID["S"], GRID["lr"]):
            s = summary(run(H, S, lr, SELECT_WORLDS), SELECT_WORLDS)
            out[f"H={H} S={S} lr={lr}"] = s
            print(f"H={H:5d} S={S} lr={lr:<6} selection mean {s['world_mean']:.3f} {s['world_mean_by_seed']} "
                  f"cpu<={s['cpu_s_per_life_max']:.1f}s numbers={s['numbers']}", flush=True)
        best = max(out, key=lambda k: out[k]["world_mean"])
        print(f"chosen on 310806-310819: {best}")
    else:
        rows = run(a.H, a.S, a.lr, SELECT_WORLDS + CHECK_WORLDS, tuple(a.seeds))
        out = {"config": {"H": a.H, "S": a.S, "lr": a.lr}, "rows": rows,
               "all_20": summary(rows, SELECT_WORLDS + CHECK_WORLDS), "not_used_for_choice_6": summary(rows, CHECK_WORLDS)}
        for k in ("all_20", "not_used_for_choice_6"):
            s = out[k]
            print(f"{k}: known {s['known_mean_over_seeds']:.1f} / {s['seen']:.0f} = world mean {s['world_mean']:.3f} "
                  f"(by seed {s['world_mean_by_seed']}), cpu mean {s['cpu_s_per_life_mean']:.1f}s max {s['cpu_s_per_life_max']:.1f}s, "
                  f"numbers={s['numbers']}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
