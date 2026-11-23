"""Score your model on the hard development worlds in data/hard-dev/ with the all-pairs measure.

Usage (repository root):  python3 tools/score_hard_dev.py predictions.json

Each world has one cue per seen object (cue_goz is a colourless image; cue_dokunma, cue_kulak, cue_koku). Answer every
object under 7 cue sets: "all" (all four senses) and each pair of senses (keys below). An object is KNOWN only if all 7
answers are the correct palette index.

predictions.json: {"310800": {"all": [...], "goz+dokunma": [...], ..., "kulak+koku": [...]}, ...}
"""
import itertools
import json
import pathlib
import sys

import numpy as np

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "hard-dev"
SENSES = ("goz", "dokunma", "kulak", "koku")
CUE_SETS = ["all"] + [f"{a}+{b}" for a, b in itertools.combinations(SENSES, 2)]


def main(path):
    pred = json.loads(pathlib.Path(path).read_text())
    known_total = seen_total = 0
    for seed in sorted(pred, key=int):
        truth = np.load(DATA / f"answers_{seed}.npz")["cue_colour"]
        ok = np.ones(truth.size, bool)
        for c in CUE_SETS:
            p = np.asarray(pred[seed][c])
            if p.shape != truth.shape:
                raise SystemExit(f"world {seed}, cue set {c}: expected {truth.size} answers, got {p.size}")
            ok &= p == truth
        known_total += int(ok.sum())
        seen_total += truth.size
        print(f"{seed}  known {int(ok.sum())} / {truth.size}")
    if seen_total:
        print(f"total  known {known_total} / {seen_total} = {known_total / seen_total:.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
