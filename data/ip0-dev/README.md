# IP0-condition development data (10 worlds, 310600–310609)

Sensory data produced by ERIKA's digital body. The body code is not public; these are its outputs. Settings match
the IP0 exam: medium difficulty, taste and smell, sharp body (touch, sound, smell and taste noise ÷ 2), 3000
encounters. These are development worlds, not the IP0 evaluation worlds.

## Files per world

**`world_<seed>.npz`** is what a learner may read.

| Key | Shape | Meaning |
|---|---|---|
| `stream_goz` | (3000, 75) | eye: 5×5 pixels × RGB, in encounter order |
| `stream_dokunma` | (3000, 6) | touch |
| `stream_kulak` | (3000, 8) | sound |
| `stream_koku` | (3000, 10) | smell |
| `stream_tat` | (3000, 5) | taste (eaten objects) |
| `stream_ic` | (3000, 2) | internal sense after eating |
| `cue_goz` | (n, 75) | exam cue: colourless (grey) image |
| `cue_dokunma` / `cue_kulak` / `cue_koku` | (n, 6 / 8 / 10) | exam cue: touch, sound, smell |
| `cue_group` | (n,) | 0 = seen in the last 150 encounters (B1), 1 = left the world early (B2) |
| `palette` | (12, 3) | the world's 12 colours (RGB) |

**`answers_<seed>.npz`** is for scoring only; a learner must not read it.

| Key | Meaning |
|---|---|
| `cue_colour` | palette index of each cue's true colour |
| `cue_object`, `stream_object`, `stream_colour` | object identities, for analysis |

## Protocol

1. Feed the stream in order, one encounter at a time; learning is allowed only here.
2. After encounter 3000, answer each cue with a palette index.
3. Run `python3 tools/score_ip0_dev.py predictions.json`.

## Reference points on these worlds

| Learner | B1 | B2 |
|---|---|---|
| ERIKA 1 (IP0 arm), fed from these files | 1.000 (310600–310601) | 1.000 |
| `tools/example_baseline.py`: stores every encounter, nearest neighbour on touch + sound + smell | 1.000 (all 10) | 1.000 |

A memory that keeps every raw encounter and has unlimited capacity solves this condition. IP0 measures retention over
a 3000-encounter stream, not discrimination; the report says so. The harder measure is the all-pairs measure on the
hard world (180 objects, normal body), where a raw nearest-neighbour memory knows 57% of objects and ERIKA 1 knows
77% (development result, not yet locked).
