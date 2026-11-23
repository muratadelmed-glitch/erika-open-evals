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

**Paired baseline (taste and smell off):**

| Arm | B1 | B2 | B3 short | B3 long | B4 unseen | Forgetting (final) |
|---|---|---|---|---|---|---|
| ERIKA (current) | 1.000 | 1.000 | 0.998 | 0.985 | 0.957 | 0.000 |
| Episodic only | 0.987 | 0.854 | 0.857 | 0.683 | 0.062 | 0.027 |
| Slow learner only | 0.373 | 0.405 | 0.000 | 0.000 | 0.975 | 0.208 |

**Ideal-observer ceiling** for B1/B2 is 1.000 in all 20 worlds.

## Reading and limits

- **This is not the neural ERIKA.** It measures the current probabilistic learner. The neuron-and-synapse ERIKA is a separate line that is still being evolved.
- **What the test measures.** The ceiling is 1.000, so the information is fully available. The test measures whether what was learned is kept and recalled: one-shot learning, then 3000 encounters with zero measured forgetting. Discrimination difficulty is not what it measures.
- **Body sharpness.** The sharp-body setting (k = 2) was chosen after inspecting already-seen development worlds. This is stated in the preregistration.
- **Not covered.** Changing-world and scale conditions are not part of IP0.
- **Forgetting checkpoints.** Forgetting is measured at 5 checkpoints only.
- **Statistics.** Single run; the world is the unit (n = 20).
- **Independent rescoring:** pending.
