# Hard-world development data (20 worlds, 310800–310819)

Sensory data produced by ERIKA's digital body. The body code is not public; these are its outputs. These are
development worlds, not locked evaluation worlds. The locked exam on 20 unseen worlds is `records/2026-11-IP1/`; its
sensory data, in the same format, are in `records/2026-11-IP1/data/`.

**World (all 20):** the hard setting of `world/dunya.py`:
`DunyaAyar(birey=30, iz_piksel=1, iz_sapma=0.04, koku=True, koku_aile=0.5)`.
- 180 stream objects, 12 colours, 3,000 encounters, one object at a time.
- Smell is on. No taste. Normal body.
- Individuals of a kind differ by one shape pixel and by N(0, 0.04) in touch, sound and smell.

`python3 tools/verify_exam_worlds.py` checks that the public generator reproduces these worlds.

## Files per world

**`world_<seed>.npz`** (a learner may read this):

- The encounter stream, in order: `stream_goz` (3000, 75; a 5×5 RGB image), `stream_dokunma` (3000, 6),
  `stream_kulak` (3000, 8), `stream_koku` (3000, 10), `stream_ic` (3000, 2; internal sense).
- One colourless cue per object seen in the stream: `cue_goz`, `cue_dokunma`, `cue_kulak`, `cue_koku`.
- `palette` (12, 3).

**`features_<seed>.npz`** (a learner may read this): the 49 processed numbers per encounter that the reference
memories and neural ERIKA 2 see.
- Contents: 25 brightness values (colourless, gain-normalised), 6 touch, 8 sound, 10 smell, scaled.
- Arrays:
  - `stream_x` (3000, 49);
  - `stream_colour`: the colour index of each encounter, which the learner observes while living;
  - `cue_x` (n, 49);
  - `cue_object`.

**`answers_<seed>.npz`** (scoring only): `cue_colour`, `cue_object`, `stream_object`.

## Measure (all pairs)

Answer every object 7 times:

- with all four senses;
- with each pair of senses (6 pairs).

An object is **known** only if all 7 answers are correct. Score it with
`python3 tools/score_hard_dev.py predictions.json`; the file's header describes the predictions format.

## Reference points (development, not locked)

All from the same internal run (`pilot/vucut/ip1.py`, DEV rehearsal, 24 November). The answers of each system are in
`predictions/<system>.json`; score any of them yourself, e.g.
`python3 tools/score_hard_dev.py data/hard-dev/predictions/erika1.json`.

| System | `predictions/` | Known / seen (20 worlds) |
|---|---|---|
| ERIKA 1 | `erika1.json` | 2792 / 3578 (0.780) |
| 5-NN over every stored encounter | `knn5.json` | 2172 / 3578 (0.607) |
| 1-NN over every stored encounter | `nn1.json` | 2081 / 3578 (0.582) |
| Slow memory only | `yavas.json` | 1300 / 3578 (0.363) |
| Fast memory only | `hizli.json` | 1000 / 3578 (0.279) |
| Neural ERIKA 2, hand-written rule, tuned | `e2_el_uyum005_t0.json` | 1927 / 3578 (0.539) |
| Neural ERIKA 2, hand-written rule | `e2_el_t0.json` | 1594 / 3578 (0.446) |
| Neural ERIKA 2, evolved rule (gen. 515) | `e2_k515_t0.json` | 1194 / 3578 (0.334) |
| Neural ERIKA 2, evolved rule (gen. 852) | `e2_k852_t0.json` | 700 / 3578 (0.196) |

The two nearest-neighbour references can be recomputed from the published features alone:
`python3 tools/reference_hard.py --check`. The result matches the internal run in every world.

The earlier 6-world release (310800–310805) is unchanged; its files are identical to the first six worlds here.
