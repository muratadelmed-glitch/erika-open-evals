# erika-open-evals

Open, preregistered memory tests for **ERIKA**, a continual-learning research system that learns with no
pre-training, no labels and no built-in knowledge. ERIKA learns only from the senses of a small digital body in a
synthetic world.

This repository holds the parts anyone should be able to inspect: the world generator, the test specification, and
the preregistrations, raw outputs and reports of locked runs. The learning system itself is not here.

## Start here

| I want to… | Go to |
|---|---|
| See the results | [`records/2026-11-IP1/REPORT.md`](records/2026-11-IP1/REPORT.md) (hard world) and [`records/2026-11-IP0/REPORT.md`](records/2026-11-IP0/REPORT.md) |
| Check everything with one command | `python3 tools/verify_all.py` (about 40 seconds; see [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)) |
| Check that the rules were fixed before the run | [`records/2026-11-IP0/PREREGISTRATION.md`](records/2026-11-IP0/PREREGISTRATION.md) (binding Turkish original: `PREREGISTRATION_tr.md`) |
| Re-score the results myself | `python3 tools/rescore_ip1.py`, `python3 tools/rescore_ip0.py` |
| Test my own model on the same exam | [`data/ip0-dev/`](data/ip0-dev/) (sensory data) + `tools/score_ip0_dev.py` |
| Test my own model on the harder all-pairs measure | [`data/hard-dev/`](data/hard-dev/) (20 worlds, with every reference's answers) + `tools/score_hard_dev.py` |
| Know what each test measures | [`tests/SPEC.md`](tests/SPEC.md) |
| Generate or inspect the worlds | [`world/`](world/) and `python3 -m world.verify` |
| Read Turkish names in code or raw data | [`GLOSSARY.md`](GLOSSARY.md) |

## Result at a glance: IP1, hard world (locked, 2026-11-24)

ERIKA lived through 3000 encounters in each of 20 worlds it had never seen, with 180 look-alike objects. Every seen
object was then asked for its colour 7 times: all senses together and each pair of senses, from a colourless cue.
An object counts as known only if all 7 answers are right. Thresholds were committed before the run.

| System | Known objects (20 worlds) | Ahead of ERIKA in |
|---|---|---|
| **ERIKA (current)** | **79.3%** (95% CI 78.3–80.4%) | — |
| 5-nearest-neighbour over every stored encounter | 62.0% | 0 of 20 worlds |
| 1-nearest-neighbour over every stored encounter | 59.8% | 0 of 20 worlds |
| Slow memory only | 35.6% | 0 of 20 worlds |
| Fast memory only | 23.5% | 0 of 20 worlds |

**Decision: PASS** (all five preregistered hypotheses). The neural ERIKA 2, measured on the same worlds without a
threshold, reaches 19–52% depending on its learning rule. ERIKA holds about 5.7× more numbers and uses about 45×
more CPU than the nearest-neighbour references; the exam tests accuracy, not efficiency. A trained reference (an
online neural network with a replay buffer, at about ERIKA's CPU budget) scores 43.2% on the 20 development worlds;
see [`data/hard-dev/`](data/hard-dev/README.md#budgets-and-a-trained-reference).

## Result at a glance: IP0 (locked, 2026-11-23)

ERIKA lived through 3000 encounters in each of 20 worlds it had never seen. It was then asked for the colour of
objects from a grey (colour-masked) image plus touch, sound and smell. The pass threshold (20-world mean ≥ 0.90 on
both endpoints) was committed before the run.

| System | B1 short-term | B2 long-term | Forgetting |
|---|---|---|---|
| **ERIKA (current)** | **1.000** | **1.000** | **0.000** |
| Episodic store only | 0.885 | 0.782 | 0.059 |
| Slow learner only | 0.379 | 0.415 | 0.207 |

**Decision: PASS.** The ideal-observer ceiling is 1.000 in every world. The test therefore measures retention and
recall over a long stream, not fine discrimination.

**Scope.** This is the current probabilistic learner, not the neural ERIKA, which is still in development. One-shot
learning is not measured. All limits are listed in the report.

## Re-score it yourself (about 1 second, standard library only)

```bash
python3 tools/rescore_ip0.py
```

The script:

- checks the SHA-256 of the raw archive and of every per-world output;
- recomputes B1/B2 for all three arms from the end-of-stream checkpoint;
- applies the preregistered rule;
- confirms the result matches the decision report written at run time.

## Repository layout

```
README.md               this page
GLOSSARY.md             Turkish names in code and raw data → English
tests/SPEC.md           what each memory test (B1–B8) measures
records/                one folder per locked run
  2026-11-IP1/            hard-world exam: preregistration, report, raw outputs, sensory data of the 20 exam worlds
  2026-11-IP0/
    PREREGISTRATION_tr.md   binding preregistration (locked before the run)
    PREREGISTRATION.md      English summary
    REPORT.md               results and limits
    raw/ip0_raw.json.gz     raw outputs + run manifest + decision report
tools/verify_all.py     runs every check below; exit 0 only if all pass (also run by CI on every push)
tools/rescore_ip1.py    independent re-scoring of IP1 from raw outputs
tools/verify_exam_worlds.py  the public generator reproduces the IP1 and hard-dev worlds
tools/reference_hard.py 1-NN / 5-NN references recomputed from published features
tools/reference_replay.py trained reference: online neural network with a replay buffer (budget-reported)
tools/rescore_ip0.py    independent re-scoring of IP0 from raw outputs
tools/score_ip0_dev.py  score your own model on data/ip0-dev/
tools/example_baseline.py  minimal nearest-neighbour learner (data format example)
data/ip0-dev/           sensory data (body outputs) for 10 development worlds, IP0 settings
data/hard-dev/          sensory data + features for 20 hard development worlds, all-pairs measure, every system's answers
data/SHA256SUMS         checksums of every published data and raw-result file
requirements.txt        pinned NumPy version used to produce every number here
tools/score_hard_dev.py score your own model on data/hard-dev/
world/                  world generator (public copy) + reference hashes
  dunya.py                generator
  verify.py               reproduces the reference worlds
```

## World generator

Requires Python 3.12+ and NumPy. The reference worlds were produced with NumPy 2.5.3.

```bash
python3 -m world.verify          # reproduces the reference worlds, prints OK
python3 -c "from world.dunya import Dunya; d = Dunya(310600); print(len(d.bireyler), d.ayar.karsilasma)"
```

Each world has hidden kinds, individuals, colours, shapes, smells, tastes, an encounter stream and an optional rule
change. The learner never sees kinds or colour names, only raw sense values.

## Principles

- **Preregistration.** Worlds, settings, thresholds and analysis are committed before a locked run. Thresholds are
  never changed afterwards. Results are published whether they pass or fail.
- **Separate data.** Development, tuning and evaluation worlds use disjoint seed ranges. Locked runs use worlds the
  learner has never seen.
- **Independent checking.** A second reviewer re-scores each locked run from its raw output (so far a separate AI
  agent, not a human), and anyone can do the same with `tools/`. An independent human review has not been done yet.
- **Honest labels.** Development results are never presented as evaluation results.

## Licence

Apache-2.0 (see `LICENSE`).
