"""Re-score the IP0 locked exam from its raw outputs, with no private code.

Usage (repository root):  python3 tools/rescore_ip0.py

What it does:
  1. Checks the SHA-256 of records/2026-11-IP0/raw/ip0_raw.json.gz against the value in REPORT.md.
  2. Checks every per-world output against the SHA-256 in the run manifest.
  3. Recomputes B1 (short-term) and B2 (long-term) colour memory for each arm from the final checkpoint (encounter 3000),
     prints the 20-world mean and worst world, and applies the preregistered rule (mean >= 0.90 for both = PASS).
  4. Compares the result with the decision report written at run time.

Raw field names are Turkish; see GLOSSARY.md.
"""
import gzip
import hashlib
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "records/2026-11-IP0/raw/ip0_raw.json.gz"
EXPECTED_SHA = "f31af26248e0c91032cd58213df3deabedff6674dfa5c3f47af209300b3a8a5d"
SYSTEM = "erika_son_bol_tam_kar_ebk"
ARMS = {SYSTEM: "ERIKA (current)", "epizodik": "Episodic only", "yavas": "Slow learner only"}
THRESHOLD = 0.90
FINAL = "3000"


def main():
    sha = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(f"archive SHA-256 {'OK' if sha == EXPECTED_SHA else 'MISMATCH ' + sha}")
    raw = json.loads(gzip.decompress(RAW.read_bytes()))
    manifest = json.loads(raw["MANIFEST.json"])
    bad = [r["dunya"] for r in manifest["kosular"]
           if hashlib.sha256(raw[f"{r['dunya']}.json"].encode()).hexdigest() != r["sha256"] or r["cikis"] != 0]
    print(f"per-world outputs: {len(manifest['kosular'])} worlds, "
          f"{'all hashes OK, all exit 0' if not bad else 'PROBLEM in ' + str(bad)}")

    worlds = manifest["dunyalar"]
    print(f"\n{'arm':<20}{'B1 mean':>9}{'B1 worst':>10}{'B2 mean':>9}{'B2 worst':>10}   (condition: taste + smell)")
    result = {}
    for arm, name in ARMS.items():
        b1, b2 = [], []
        for w in worlds:
            (run,) = json.loads(raw[f"{w}.json"])
            final = run["kollar"][arm]["denetim"][FINAL]
            b1.append(final["m10_kisa_ornek_dogruluk"])
            b2.append(final["m10_uzun_ornek_dogruluk"])
        result[arm] = (statistics.fmean(b1), statistics.fmean(b2))
        print(f"{name:<20}{result[arm][0]:>9.3f}{min(b1):>10.3f}{result[arm][1]:>9.3f}{min(b2):>10.3f}")

    b1, b2 = result[SYSTEM]
    decision = "PASS" if b1 >= THRESHOLD and b2 >= THRESHOLD else "FAIL"
    print(f"\npreregistered rule: mean B1 and B2 >= {THRESHOLD} over {len(worlds)} worlds -> {decision}")

    report = json.loads(raw["../ip0_degerlendirme_rapor.json"])
    same = (report["karar"] == {"B1_kisa": decision, "B2_uzun": decision}
            and abs(report["toplu"]["B1_kisa"]["ortalama"] - b1) < 1e-12
            and abs(report["toplu"]["B2_uzun"]["ortalama"] - b2) < 1e-12)
    print(f"matches the decision report written at run time: {'yes' if same else 'NO'}")
    return 0 if sha == EXPECTED_SHA and not bad and same else 1


if __name__ == "__main__":
    sys.exit(main())
