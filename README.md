# erika-open-evals

Open, pre-registered memory tests and world generator for continual-learning AI (ERIKA project).

ERIKA is a research system that learns with no pre-training, labels or built-in knowledge, only from the senses of
a small digital body living in a synthetic world. The learning system and the digital body are **not** in this
repository. What is here is the part we want anyone to be able to inspect and reuse:

| Folder | What | Status |
|---|---|---|
| `world/` | The world generator: hidden kinds, individuals, colours, shapes, smells, tastes, an encounter stream, optional rule change | published; `python3 -m world.verify` checks it against reference worlds |
| `tests/` | Specification of the memory tests (what is measured, how, chance levels, ceilings) | draft specification |
| `records/` | Pre-registrations (locked before a run) and the raw results and reports of locked runs | empty until the first locked run |

## Principles

- **Pre-registration.** Every locked evaluation is written down (worlds, settings, thresholds, analysis) and
  committed *before* the run. Thresholds are never changed afterwards; results are published whether or not they
  meet them.
- **Separation of data.** Development, tuning and evaluation worlds are disjoint seed ranges. Locked evaluations use
  worlds the learner has never seen.
- **Independent checking.** Each locked run is re-scored from its raw output by a second reviewer.
- **Honest labels.** Development results are labelled `DEV_ONLY` and are never presented as evaluation results.

## Running the world generator

Requires Python 3.12+ and NumPy (reference worlds were produced with NumPy 2.5.3).

```bash
python3 -m world.verify          # reproduces the reference worlds (prints OK)
python3 -c "from world.dunya import Dunya; d = Dunya(310600); print(len(d.bireyler), d.ayar.karsilasma)"
```

Source comments are in Turkish (the project's working language).

## Licence

Apache-2.0 (see `LICENSE`).
