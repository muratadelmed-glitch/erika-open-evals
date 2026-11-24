# Reproducibility: what you can check, and what you cannot

ERIKA's learning code and body code are not public (see the main README). This page says exactly which claims you can
verify from this repository alone, and how.

## One command

```bash
pip install -r requirements.txt      # NumPy 2.5.3, the version that produced every number here
python3 tools/verify_all.py          # about 40 seconds on a laptop; exit code 0 only if every check passes
```

The same command runs in CI on every push (`.github/workflows/verify.yml`).

## What each check proves

| Check | What it shows | Tool |
|---|---|---|
| Data checksums | No published data or raw-result file changed since release (`data/SHA256SUMS`) | `verify_all.py` |
| World generator | The public generator reproduces the reference worlds bit for bit | `python3 -m world.verify` |
| Exam worlds | The 20 IP1 exam worlds and the 20 hard development worlds are exactly what the public generator makes for those seeds (encounter order, colours, palette) | `tools/verify_exam_worlds.py` |
| IP0 re-score | The IP0 decision follows from the raw outputs and the preregistered rule | `tools/rescore_ip0.py` |
| IP1 re-score | The IP1 decision follows from the raw answers and the preregistered rule, and the run was the locked one (preregistration hash, lock commit, kernel hash, every world's output hash) | `tools/rescore_ip1.py` |
| Example baseline | A memory that stores everything scores 1.000 / 1.000 on IP0-style data (why IP0 alone is not enough) | `tools/example_baseline.py` + `tools/score_ip0_dev.py` |
| Reference memories | The 1-NN and 5-NN references on the hard development worlds, recomputed from published features, match the internal run in every world | `tools/reference_hard.py --check` |

## What you can do beyond checking

- Run your own learner on the same sensory data, in three settings:
  - IP0-style worlds (`data/ip0-dev/`);
  - hard development worlds (`data/hard-dev/`);
  - the 20 IP1 exam worlds (`records/2026-11-IP1/data/`; these are public now, so no longer unseen).
- Score it with the same tools.
- Compare your learner with every system's answers, object by object. ERIKA 1, both single-memory versions, both
  references and four neural ERIKA 2 rules are included (`data/hard-dev/predictions/`, and raw answers inside
  `records/2026-11-IP1/raw/`).

## What you cannot check here

- **That ERIKA's learner produced these answers.** The learning code and the body code are closed. The integrity of a
  locked run rests on three things:
  - a preregistration committed before the run, and a lock commit that changes only its status line;
  - a tool that opens evaluation worlds only under a locked preregistration, refuses to run if the measured code or the
    compiled kernel changed after the lock, and records the run so it cannot be repeated;
  - an independent agent audit before the lock.
  
  An independent human or laboratory rerun of ERIKA itself has not been done.
- **The processing from raw senses to features** (brightness extraction, gain normalisation). The outputs are
  published (`features_<seed>.npz`); the code is part of the closed body.

## Versions

- Python 3.12+ (results produced with 3.13.18), NumPy 2.5.3.
- Locked runs record their environment in the run manifest: Python, NumPy, machine, git commit, kernel hash.
