"""Check that this public world generator reproduces the reference worlds (seeds 310600-310609).

Usage (repository root):  python3 -m world.verify
"""
import hashlib
import json
import pathlib
import sys

import numpy as np

from world.dunya import Dunya, DunyaAyar

SETTINGS = {
    "varsayilan": DunyaAyar(),
    "orta_zor_tat_koku": DunyaAyar(birey=30, iz_piksel=1, iz_sapma=0.04, koku=True, tat=True, koku_aile=0.5,
                                   tat_sonuc=0.5),
}


def fingerprint(d):
    h = hashlib.sha256()
    h.update(np.asarray(d.akis).tobytes())
    h.update(np.asarray(d.palet).tobytes())
    for b in d.bireyler:
        h.update(repr((b.no, b.tur, b.renk, b.emekli, b.test, b.yeni_kural)).encode())
        h.update(np.asarray(b.maske).tobytes())
    return h.hexdigest()


def main():
    ref = json.loads((pathlib.Path(__file__).parent / "reference_hashes.json").read_text())
    bad = [(s, k) for s, v in ref.items() for k, h in v.items() if fingerprint(Dunya(int(s), SETTINGS[k])) != h]
    print("OK" if not bad else f"MISMATCH: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
