# IP1 preregistration — English summary

The binding text is the Turkish original, `PREREGISTRATION_tr.md`. It is byte-identical to the locked file in the
development repository (SHA-256 `2d2ab017d52a7ae5a89efc2545087101361eac5b11ecde8ed35fc25b1e3fce35`), locked by commit
`e435bf8`. This page summarises it; if they differ, the Turkish text holds.

## Question

On 6 development worlds, ERIKA 1 knew 77.1% of objects in the hard world under the all-pairs measure. The question:
does this hold on 20 evaluation worlds it has never seen? And does ERIKA 1 stay ahead of:
- memories that store every encounter;
- its own single-memory versions?

## Worlds

- Evaluation worlds 312021–312040. IP0 used 312001–312020; 312000 is quarantined.
- Hard setting: `DunyaAyar(birey=30, iz_piksel=1, iz_sapma=0.04, koku=True, koku_aile=0.5)`. All other fields default.
  - 180 stream individuals, 12 colours, 3,000 encounters.
  - Smell is on, half shared within a family. No taste.
  - Each individual deviates from its kind by 1 flipped shape pixel and by N(0, 0.04) in texture, sound and smell.
- Normal body.

## Measure

- Every object seen in the stream is asked 7 times: all four senses, and each of the 6 sense pairs.
- The cue is colourless, with fresh noise.
- Known = all 7 answers are the right palette colour. Score = known / seen.
- The world is the statistical unit.

## Systems

| Arm | Role |
|---|---|
| `erika1`: ERIKA 1 (`erika_son_bol_tam_kar_ebk`, the IP0 system) | primary |
| `hizli`: fast memory only; `yavas`: slow memory only | references |
| `nn1`: 1-nearest neighbour over every stored encounter | reference |
| `knn5`: 5-nearest-neighbour majority vote, same memory | reference |
| `e2_<rule>_t<seed>`: neural ERIKA 2, 4 rules × 3 network seeds | descriptive, no threshold |

- k = 5 was chosen on development worlds 310806–310819 as the best of {1, 3, 5, 9, 15, 25}.
- Tie rule: if the vote is tied and the nearest neighbour's colour is among the tied colours, choose it; otherwise
  choose the smallest tied colour index.

## Decision rule (fixed before the run)

| | Hypothesis | Pass if |
|---|---|---|
| H1 | ERIKA 1 world mean | ≥ 0.70 |
| H2a / H2b | ERIKA 1 knows strictly more objects than 1-NN / 5-NN | in ≥ 16 of 20 worlds |
| H3a / H3b | ERIKA 1 knows strictly more objects than fast-only / slow-only | in ≥ 16 of 20 worlds |

- **Overall:** PASS only if all five pass. Otherwise FAIL.
- **INCONCLUSIVE** if any world is missing or crashed, if a hash does not match, or if a recount disagrees. No world
  is replaced and no run is repeated.
- An error in an ERIKA 2 arm does not affect H1–H3.

## Rationale (from development data, 20 worlds 310800–310819)

- ERIKA 1 world mean was 0.780 (95% interval [0.764, 0.796]); the worst world was 0.697. The threshold of 0.70
  applies to the mean, about 8 points below the development mean.
- ERIKA 1 was ahead of every reference in 20 of 20 development worlds.
- 16 of 20 corresponds to a one-sided sign test p ≈ 0.006.

## Known limits written before the run

- One code version, one run per world, small synthetic worlds.
- The references keep all raw information but are not trained learners.
- ERIKA 1 holds more numbers and uses more CPU than the references; the exam tests accuracy, not efficiency.
