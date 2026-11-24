# IP0 report: PASS

**Run:** 2026-11-23, 03:04–03:25 UTC, in a clean detached checkout of the lock commit.
- 20/20 worlds exited 0.
- Raw outputs: `raw/ip0_raw.json.gz` (SHA-256 `f31af26248e0c91032cd58213df3deabedff6674dfa5c3f47af209300b3a8a5d`). It holds the per-world JSON, stderr, the run manifest and the decision report.

## Decision (preregistered rule)

| Endpoint | 20-world mean | 95% CI (world bootstrap) | Worst world | Threshold | Result |
|---|---|---|---|---|---|
| B1 short-term colour memory | 1.000 | [1.000, 1.000] | 1.000 | ≥ 0.90 | **PASS** |
| B2 long-term colour memory | 1.000 | [1.000, 1.000] | 1.000 | ≥ 0.90 | **PASS** |

## Secondary results (descriptive)

**Taste + smell condition (primary condition):**

| Arm | B1 | B2 | B3 short | B3 long | B4 unseen | Forgetting (final) | Forgetting (worst) |
|---|---|---|---|---|---|---|---|
| ERIKA (current) | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 0.000 | 0.000 |
| Episodic only | 0.885 | 0.782 | 0.572 | 0.475 | 0.106 | 0.059 | 0.103 |
| Slow learner only | 0.379 | 0.415 | 0.000 | 0.000 | 1.000 | 0.207 | 0.338 |

**Paired baseline (taste and smell off; ERIKA's worst world on B4 here is 0.632, world 312016):**

| Arm | B1 | B2 | B3 short | B3 long | B4 unseen | Forgetting (final) |
|---|---|---|---|---|---|---|
| ERIKA (current) | 1.000 | 1.000 | 0.998 | 0.985 | 0.957 | 0.000 |
| Episodic only | 0.987 | 0.854 | 0.857 | 0.683 | 0.062 | 0.027 |
| Slow learner only | 0.373 | 0.405 | 0.000 | 0.000 | 0.975 | 0.208 |

**Ideal-observer ceiling** for B1/B2 is 1.000 in all 20 worlds.

## Reading and limits

*Corrected 2026-11-23 after re-scoring by a separate AI agent (numbers and PASS unchanged). The B1/B2 recall cue shows the object's shape with its colour masked (grey image), plus touch, sound and smell; only B3/B4 use a cue with no image. An earlier version of this report also claimed one-shot learning, which IP0 does not measure.*

- **This is not the neural ERIKA.** It measures the current probabilistic learner. The neuron-and-synapse ERIKA is a separate line that is still being evolved.
- **What the test measures.** The ceiling is 1.000, so the information is fully available. The test measures whether learned colour associations are kept and recalled over 3000 encounters, with zero measured forgetting. Discrimination difficulty is not what it measures.
- **What it does not measure.** It does not measure one-shot learning. In development worlds with the same settings, tested individuals were mostly seen many times (B1 group: median about 20 sightings, none seen only once; B2 group: median about 5, about 5% seen once).
- **Body sharpness.** The sharp-body setting (k = 2) was chosen after inspecting already-seen development worlds. This is stated in the preregistration.
- **Not covered.** Changing-world and scale conditions are not part of IP0.
- **Forgetting checkpoints.** Forgetting is measured at 5 checkpoints only.
- **Statistics.** Single run; the world is the unit (n = 20).
- **Re-scoring (status 2026-11-24):** re-scored from the raw archive by a separate AI agent (not the one that ran the
  exam) and by `tools/rescore_ip0.py`, which anyone can run (`tools/verify_all.py`). No independent human or laboratory
  has re-scored or rerun it yet. ERIKA's learning code is closed, so the run itself cannot be repeated outside the project.
