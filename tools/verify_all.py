"""Run every public check in this repository with one command and print a summary.

Usage (repository root):  python3 tools/verify_all.py

Checks, in order:
  1. data/SHA256SUMS: every published data and raw-result file matches its recorded SHA-256.
  2. world.verify: the public world generator reproduces the reference worlds.
  3. rescore_ip0: the IP0 locked exam re-scored from its raw archive (decision must be PASS, as recorded).
  4. rescore_ip1: the IP1 locked exam re-scored from its raw archive (decision must match the recorded one).
  5. example baseline on data/ip0-dev: the store-everything example must score 1.000 / 1.000 (documented).
  6. reference_hard.py: the 1-NN and 5-NN store-everything references recomputed on data/hard-dev from published
     features must match the recorded counts.
  7. verify_exam_worlds.py: the public generator reproduces the 20 IP1 exam worlds and the 20 hard-dev worlds.

Exit code 0 only if every check passes. Needs Python 3.12+ and NumPy (see requirements.txt).
"""
import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def sha256sums():
    bad, n = [], 0
    for line in (ROOT / "data" / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        n += 1
        p = ROOT / name.strip()
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            bad.append(name)
    return (not bad), f"{n} files, {'all match' if not bad else 'MISMATCH: ' + ', '.join(bad)}"


def run(args, must_contain):
    p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    out = p.stdout + p.stderr
    ok = p.returncode == 0 and all(s in out for s in must_contain)
    last = [l for l in out.strip().splitlines() if l.strip()]
    return ok, (last[-1] if last else f"exit {p.returncode}")


def main():
    checks = [
        ("data checksums", sha256sums),
        ("world generator", lambda: run(["-m", "world.verify"], ["OK"])),
        ("IP0 re-score", lambda: run(["tools/rescore_ip0.py"], ["all hashes OK", "matches the decision report"])),
        ("IP1 re-score", lambda: run(["tools/rescore_ip1.py"], ["all hashes OK", "matches the decision report"])),
        ("IP0 example baseline", lambda: _baseline()),
        ("hard-dev references", lambda: run(["tools/reference_hard.py", "--check"], ["match the recorded counts"])),
        ("exam worlds regenerated", lambda: run(["tools/verify_exam_worlds.py"], ["all match the published files"])),
    ]
    failed = 0
    for name, fn in checks:
        try:
            ok, msg = fn()
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f"{type(e).__name__}: {e}"
        failed += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
    return 1 if failed else 0


def _baseline():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        pred = pathlib.Path(t) / "pred.json"
        p = subprocess.run([sys.executable, "tools/example_baseline.py"], cwd=ROOT, capture_output=True, text=True)
        if p.returncode != 0:
            return False, p.stderr.strip().splitlines()[-1]
        pred.write_text(p.stdout)
        return run(["tools/score_ip0_dev.py", str(pred)], ["B1 1.000  B2 1.000"])


if __name__ == "__main__":
    sys.exit(main())
