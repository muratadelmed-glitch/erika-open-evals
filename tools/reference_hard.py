"""Store-everything reference memories on the hard development worlds, recomputed from published features only.

Usage (repository root):
  python3 tools/reference_hard.py            # print known / seen per world for 1-NN and 5-NN
  python3 tools/reference_hard.py --check    # also compare with the counts recorded by the internal run

The reference stores every encounter of the stream (49 features + the colour seen) and answers a cue with the colour
of its nearest stored encounter (1-NN) or the majority colour of the 5 nearest (5-NN; tie: the nearest neighbour's
colour if it is among the tied colours, otherwise the smallest tied colour index). Features are z-scored with the
stream mean and standard deviation (+1e-6). Pair cues use only the columns of the two senses. The measure is the same
all-pairs measure as tools/score_hard_dev.py: an object is known only if all 7 answers are right.

Features (data/hard-dev/features_<seed>.npz) are the body's processed outputs that the references and the neural ERIKA 2
see: 25 brightness values (colourless, gain-normalised), 6 touch, 8 sound, 10 smell, scaled.
"""
import itertools
import pathlib
import sys

import numpy as np

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "hard-dev"
BLOCKS = (("goz", 25), ("dokunma", 6), ("kulak", 8), ("koku", 10))
# Recorded by the internal run (pilot/vucut/ip1.py, DEV rehearsal, archive 2026-11-24_IP1_DEV_PROVA.json.gz).
RECORDED = {
    "1-NN": {310800: 115, 310801: 98, 310802: 101, 310803: 105, 310804: 105, 310805: 86, 310806: 108, 310807: 110,
             310808: 115, 310809: 105, 310810: 104, 310811: 86, 310812: 102, 310813: 116, 310814: 113, 310815: 119,
             310816: 107, 310817: 102, 310818: 89, 310819: 95},
    "5-NN": {310800: 107, 310801: 100, 310802: 107, 310803: 111, 310804: 112, 310805: 97, 310806: 113, 310807: 120,
             310808: 108, 310809: 97, 310810: 113, 310811: 93, 310812: 111, 310813: 122, 310814: 113, 310815: 120,
             310816: 111, 310817: 104, 310818: 104, 310819: 109},
}


def masks():
    edges, i = {}, 0
    for name, n in BLOCKS:
        edges[name] = (i, i + n)
        i += n
    out = {"all": np.ones(i, bool)}
    for a, b in itertools.combinations([n for n, _ in BLOCKS], 2):
        m = np.zeros(i, bool)
        for k in (a, b):
            m[edges[k][0]:edges[k][1]] = True
        out[f"{a}+{b}"] = m
    return out


def known(seed, k):
    f = np.load(DATA / f"features_{seed}.npz")
    truth = np.load(DATA / f"answers_{seed}.npz")
    if not np.array_equal(f["cue_object"], truth["cue_object"]):
        raise SystemExit(f"{seed}: feature and answer files disagree on the object list")
    X, colour = f["stream_x"], f["stream_colour"].astype(int)
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    ok = np.ones(len(f["cue_x"]), bool)
    for m in masks().values():
        for i, z in enumerate((f["cue_x"] - mu) / sd):
            d = ((Z[:, m] - z[m]) ** 2).sum(1)
            if k == 1:
                pred = colour[np.argmin(d)]
            else:
                idx = np.argsort(d, kind="stable")[:k]
                votes = np.bincount(colour[idx], minlength=len(np.load(DATA / f"world_{seed}.npz")["palette"]))
                best = np.flatnonzero(votes == votes.max())
                pred = best[0] if len(best) == 1 else (colour[idx[0]] if colour[idx[0]] in best else best[0])
            ok[i] &= pred == truth["cue_colour"][i]
    return int(ok.sum()), ok.size


def main(check):
    seeds = sorted(int(p.stem.split("_")[1]) for p in DATA.glob("features_*.npz"))
    bad = []
    for name, k in (("1-NN", 1), ("5-NN", 5)):
        tot = n_tot = 0
        for s in seeds:
            kn, n = known(s, k)
            tot, n_tot = tot + kn, n_tot + n
            if check and RECORDED[name].get(s) != kn:
                bad.append((name, s, kn, RECORDED[name].get(s)))
        print(f"{name}: known {tot} / {n_tot} = {tot / n_tot:.3f} over {len(seeds)} worlds")
    if check:
        print("all counts match the recorded counts" if not bad else f"MISMATCH: {bad}")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
