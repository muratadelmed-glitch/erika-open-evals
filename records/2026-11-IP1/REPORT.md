# IP1: locked memory exam in the hard world — report

**Decision: PASS.** Run once, on 24 November 2026, on 20 evaluation worlds (312021–312040) that no tool had opened
before. The thresholds were committed before the run (lock commit `e435bf8`).

## What was tested

ERIKA 1 (the current hand-written two-memory learner, the same system as in IP0) lives through 3,000 encounters in a
"hard" world:
- 180 objects, 12 colours and a sense of smell;
- individuals of a kind differ by one pixel of shape and a small deviation in touch, sound and smell.

Afterwards every object it saw is asked for its colour 7 times: with all four senses together and with each pair of
senses (6 pairs). The cue image is colourless. An object counts as **known** only if all 7 answers are right.

This is a much stricter test than IP0. A memory that simply stores every encounter scores 100% on IP0, but only about
60% here.

## Results (20 worlds, 3,585 seen objects)

| System | Known / seen | World mean | 95% interval (world bootstrap) | Worst world |
|---|---|---|---|---|
| **ERIKA 1** | **2844 / 3585** | **0.793** | [0.783, 0.804] | 0.747 |
| 5-nearest-neighbour, stores every encounter | 2223 / 3585 | 0.620 | [0.604, 0.638] | 0.550 |
| 1-nearest-neighbour, stores every encounter | 2143 / 3585 | 0.598 | [0.578, 0.617] | 0.489 |
| Slow memory only (ERIKA 1 without fast memory) | 1277 / 3585 | 0.356 | [0.305, 0.402] | 0.056 |
| Fast memory only (ERIKA 1 without slow memory) | 843 / 3585 | 0.235 | [0.204, 0.265] | 0.078 |

| Preregistered hypothesis | Result | Threshold | Decision |
|---|---|---|---|
| H1: ERIKA 1 world mean | 0.793 | ≥ 0.70 | PASS |
| H2a: ERIKA 1 ahead of 1-NN, per world | 20 / 20 worlds (smallest margin 14 objects) | ≥ 16 / 20 | PASS |
| H2b: ERIKA 1 ahead of 5-NN, per world | 20 / 20 (smallest margin 15) | ≥ 16 / 20 | PASS |
| H3a: ERIKA 1 ahead of fast memory only | 20 / 20 (smallest margin 82) | ≥ 16 / 20 | PASS |
| H3b: ERIKA 1 ahead of slow memory only | 20 / 20 (smallest margin 54) | ≥ 16 / 20 | PASS |

One-sided sign test for each comparison: p = 9.5 × 10⁻⁷.

**Development numbers held on unseen worlds.** The same tool on 20 development worlds (310800–310819) gave:
- ERIKA 1: 0.780;
- 5-NN: 0.607;
- 1-NN: 0.582;
- slow memory only: 0.363;
- fast memory only: 0.279.

### Neural ERIKA 2 (descriptive; no threshold was set)

Four learning rules, each run with three network seeds:

| Rule | Seeds 0 / 1 / 2 | Mean |
|---|---|---|
| Evolved rule, generation 515 | 0.320 / 0.326 / 0.314 | 0.320 |
| Evolved rule, generation 852 (latest) | 0.189 / 0.189 / 0.194 | 0.191 |
| Hand-written rule, untuned | 0.447 / 0.449 / 0.446 | 0.447 |
| Hand-written rule, one setting tuned on development worlds | 0.516 / 0.516 / 0.517 | 0.516 |

- The neural version is not yet at ERIKA 1's level, nor at the store-everything references' level.
- The network seed changes results by at most 0.012.

## Memory and compute (descriptive)

| System | CPU seconds per life (learning + exam) | Numbers held after the life |
|---|---|---|
| ERIKA 1 | 13.5 | 855,168 |
| 1-NN / 5-NN | 0.3 / 0.5 | 150,098 |
| Neural ERIKA 2 | 5–8 | 1.9–2.1 million |

- The store-everything references keep every raw encounter, so they hold all the information the world provided.
  ERIKA 1's advantage therefore does not come from seeing more data.
- But ERIKA 1 holds about 5.7 times as many numbers and uses about 45 times as much CPU. **This exam tests accuracy,
  not efficiency.**

## Limits

- One code version, one run per world. The worlds are small and synthetic; nothing here shows generalisation to other
  kinds of world.
- The references are memories, not trained learners. Stronger references (for example a classifier trained offline on
  the whole stream) were not part of this exam.
- The k of the k-NN reference (k = 5) was chosen on development worlds 310806–310819. The choice was made before
  ERIKA 1 ran on those worlds, and it strengthens the reference.
- ERIKA's learning code is not public. What you can check yourself:
  - the raw outputs (every answer of every system);
  - the sensory data of all 20 exam worlds;
  - that the public world generator reproduces these worlds;
  - the decision.

## Integrity

- **Preregistration:** `PREREGISTRATION_tr.md` (binding Turkish original, byte-identical to the locked file; SHA-256
  `2d2ab017…3fce35`). English summary: `PREREGISTRATION.md`.
- **Lock commit:** `e435bf8`. It changes only the status line.
- **Locked code:** the evaluation tool, the learners, the world and the Rust kernel of ERIKA 2 (SHA-256 `89762ce1…f8d8`).
  The tool refuses to run if any of these change after the lock.
- **Before the lock:** an independent AI-agent audit (a separate agent, not a human) found 1 critical, 5 important and 5 minor issues. All were fixed
  before locking. The critical one was a formatting error that would have made the tool refuse to run.
- **Run:** the tool opens evaluation worlds only with a locked preregistration. A run record committed right after the
  run blocks any second locked run.
- **Raw archive:** `raw/ip1_raw.json.gz`, SHA-256 `a967552c…0c87`; run manifest SHA-256 `059e2386…2f6b`.
- **Not yet done:** an independent human or laboratory review. ERIKA's learning code is closed, so the run itself
  cannot be repeated outside the project; the answers, the decision and the worlds can.

## Re-score it yourself

```bash
python3 tools/rescore_ip1.py          # hashes, provenance, recount from raw answers, preregistered rule
python3 tools/verify_exam_worlds.py   # the public generator reproduces all 20 exam worlds
```

Sensory data of the exam worlds are in `data/` (same format as `data/hard-dev/`). You can run your own model on them
and score it with `tools/score_hard_dev.py`. These worlds are no longer unseen: they are now public.
