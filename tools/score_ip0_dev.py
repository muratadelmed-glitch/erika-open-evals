"""Score your model on the IP0-condition development worlds in data/ip0-dev/.

Usage (repository root):  python3 tools/score_ip0_dev.py predictions.json

predictions.json: {"310600": [palette index for each cue, in file order], "310601": [...], ...}
Worlds you leave out are skipped. Prints B1 (recent objects) and B2 (objects that left the world) per world and the
mean over the scored worlds. One answer per cue, so this equals IP0's mode accuracy, not its sample accuracy.
"""
import json
import pathlib
import sys

import numpy as np

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "ip0-dev"


def main(path):
    pred = json.loads(pathlib.Path(path).read_text())
    rows = []
    for seed in sorted(pred, key=int):
        w = np.load(DATA / f"world_{seed}.npz")
        a = np.load(DATA / f"answers_{seed}.npz")
        p = np.asarray(pred[seed])
        if p.shape != a["cue_colour"].shape:
            raise SystemExit(f"world {seed}: expected {a['cue_colour'].size} answers, got {p.size}")
        ok = p == a["cue_colour"]
        g = w["cue_group"]
        rows.append((seed, ok[g == 0].mean(), ok[g == 1].mean()))
        print(f"{seed}  B1 {rows[-1][1]:.3f}  B2 {rows[-1][2]:.3f}")
    if rows:
        print(f"mean over {len(rows)} worlds  B1 {np.mean([r[1] for r in rows]):.3f}  "
              f"B2 {np.mean([r[2] for r in rows]):.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
