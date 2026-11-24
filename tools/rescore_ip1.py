"""Re-score the IP1 locked exam (hard world, all-pairs measure) from its raw outputs, with no private code.

Usage (repository root):  python3 tools/rescore_ip1.py

What it does:
  1. Checks the SHA-256 of records/2026-11-IP1/raw/ip1_raw.json.gz and of the run manifest against REPORT.md.
  2. Checks every per-world output against the SHA-256 in the manifest, and that the run was the locked one
     (not a development run, preregistration SHA-256 and lock commit as recorded, Rust kernel SHA-256 as expected).
  3. Checks that the published answer files (records/2026-11-IP1/data/answers_<seed>.npz) agree with the raw outputs.
  4. Recomputes "known" (all 7 answers right) for every arm from the stored predictions and answers, prints the table,
     and applies the preregistered rule: H1 ERIKA 1 world mean >= 0.70; H2a/H2b/H3a/H3b ERIKA 1 strictly ahead of
     1-NN, 5-NN, fast-only, slow-only in at least 16 of 20 worlds.
  5. Compares the decision with the report written at run time.

Raw field names are Turkish; see GLOSSARY.md.
"""
import gzip
import hashlib
import json
import pathlib
import statistics
import sys
from math import comb

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
REC = ROOT / "records/2026-11-IP1"
RAW = REC / "raw/ip1_raw.json.gz"
EXPECTED = {
    "archive": "a967552ccc24241fe69d62a49de9a679dc9951b30cf400aedad248d6275b0c87",
    "manifest": "059e2386fb08bdec6c2dfc467ffd9ea924ad00545e5a14b2a3e0986c1b842f6b",
    "preregistration": "2d2ab017d52a7ae5a89efc2545087101361eac5b11ecde8ed35fc25b1e3fce35",
    "lock_commit": "e435bf8256625793acee07ca9c767ce6d3ab32aa",
    "rust_kernel": "89762ce13d242f28efd9525363795d80ca4d3c103b47b346209c3950e7f6f8d8",
}
NAMES = {"erika1": "ERIKA 1", "knn5": "5-NN store-everything", "nn1": "1-NN store-everything",
         "yavas": "Slow memory only", "hizli": "Fast memory only"}
RULES = (("H2a", "nn1"), ("H2b", "knn5"), ("H3a", "hizli"), ("H3b", "yavas"))
H1, SIGN = 0.70, 16


def main():
    ok = True
    blob = RAW.read_bytes()
    a = hashlib.sha256(blob).hexdigest() == EXPECTED["archive"]
    raw = json.loads(gzip.decompress(blob))
    m_text = raw["MANIFEST.json"]
    m_ok = hashlib.sha256(m_text.encode()).hexdigest() == EXPECTED["manifest"]
    man = json.loads(m_text)
    print(f"archive SHA-256 {'OK' if a else 'MISMATCH'}; manifest SHA-256 {'OK' if m_ok else 'MISMATCH'}")
    prov = (not man["dev"] and man["on_kayit"]["sha256"] == EXPECTED["preregistration"]
            and man["on_kayit"]["kilit_commit"] == EXPECTED["lock_commit"] == man["git"]
            and man["rust_so_sha256"] == EXPECTED["rust_kernel"])
    bad = [r["dunya"] for r in man["kosular"]
           if r["cikis"] != 0 or hashlib.sha256(raw[f"{r['dunya']}.json"].encode()).hexdigest() != r["sha256"]]
    print(f"locked-run provenance {'OK' if prov else 'PROBLEM'}; per-world outputs: {len(man['kosular'])} worlds, "
          f"{'all hashes OK, all exit 0' if not bad else 'PROBLEM in ' + str(bad)}")
    ok &= a and m_ok and prov and not bad

    worlds = {w: json.loads(raw[f"{w}.json"]) for w in man["dunyalar"]}
    data_bad = []
    for w, o in worlds.items():
        p = REC / "data" / f"answers_{w}.npz"
        if p.exists():
            z = np.load(p)
            if not (np.array_equal(z["cue_colour"], o["cevap"]) and np.array_equal(z["cue_object"], o["gorulen"])):
                data_bad.append(w)
        else:
            data_bad.append(w)
    print(f"published answer files agree with raw outputs: {'yes' if not data_bad else 'NO ' + str(data_bad)}")
    ok &= not data_bad

    known = {}
    for arm in worlds[man["dunyalar"][0]]["kollar"]:
        known[arm] = {}
        for w, o in worlds.items():
            if "tahmin" not in o["kollar"][arm]:
                continue
            truth = np.array(o["cevap"])
            right = np.ones(truth.size, bool)
            for c in o["ipucu_kumeleri"]:
                right &= np.array(o["kollar"][arm]["tahmin"][c]) == truth
            known[arm][w] = (int(right.sum()), truth.size)
    print("\narm                       known / seen   world mean  worst")
    for arm in [*NAMES, *[k for k in known if k not in NAMES]]:
        v = known[arm]
        k, n = sum(x for x, _ in v.values()), sum(y for _, y in v.values())
        rates = [x / y for x, y in v.values()]
        print(f"{NAMES.get(arm, arm):25s} {k:5d} / {n:5d}   {statistics.mean(rates):.3f}       {min(rates):.3f}")

    decision = {"H1": "PASS" if statistics.mean(x / y for x, y in known["erika1"].values()) >= H1 else "FAIL"}
    for h, ref in RULES:
        wins = sum(known["erika1"][w][0] > known[ref][w][0] for w in worlds)
        decision[h] = "PASS" if wins >= SIGN else "FAIL"
        p = sum(comb(len(worlds), i) for i in range(wins, len(worlds) + 1)) / 2 ** len(worlds)
        print(f"{h}: ERIKA 1 ahead of {NAMES[ref]} in {wins}/{len(worlds)} worlds (one-sided sign test p = {p:.2g})")
    overall = "PASS" if all(v == "PASS" for v in decision.values()) else "FAIL"
    print(f"\npreregistered rule -> {overall} ({', '.join(f'{k} {v}' for k, v in decision.items())})")
    recorded = json.loads(raw["rapor.json"])
    same = recorded["genel"] == overall and all(recorded["karar"][k]["sonuc"] == v for k, v in decision.items())
    print(f"matches the decision report written at run time: {'yes' if same else 'NO'}")
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
