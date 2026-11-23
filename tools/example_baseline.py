"""Minimal example learner on data/ip0-dev/: a nearest-neighbour memory over touch + sound + smell.

Usage (repository root):  python3 tools/example_baseline.py > /tmp/pred.json && python3 tools/score_ip0_dev.py /tmp/pred.json

It reads only world_*.npz (never answers_*.npz). Each encounter is stored with the colour seen by the eye (mean RGB of
bright pixels, snapped to the palette); a cue is answered with the colour of the closest stored encounter.
It is a reference point for the data format, not one of the IP0 arms.
"""
import json
import pathlib

import numpy as np

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "ip0-dev"
SENSES = ("dokunma", "kulak", "koku")


def seen_colour(eye, palette):
    img = eye.reshape(25, 3)
    bright = img.mean(1) > 0.18
    rgb = img[bright].mean(0) if bright.any() else img.mean(0)
    return int(np.argmin(((palette - rgb) ** 2).sum(1)))


out = {}
for f in sorted(DATA.glob("world_*.npz")):
    w = np.load(f)
    X = np.hstack([w[f"stream_{s}"] for s in SENSES])
    colour = np.array([seen_colour(e, w["palette"]) for e in w["stream_goz"]])
    C = np.hstack([w[f"cue_{s}"] for s in SENSES])
    nearest = ((C[:, None, :] - X[None, :, :]) ** 2).sum(2).argmin(1)
    out[f.stem.split("_")[1]] = colour[nearest].tolist()
print(json.dumps(out))
