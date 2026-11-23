# Hard-world development data (6 worlds, 310800–310805)

Sensory data produced by ERIKA's digital body. The body code is not public; these are its outputs.

**World:** 180 objects, 3000 encounters, smell, individuals differ by about 1 pixel. Normal body; no taste. These are
development worlds, not locked evaluation worlds.

## Files per world

**`world_<seed>.npz`** (a learner may read this):

- `stream_goz` (3000, 75), `stream_dokunma` (3000, 6), `stream_kulak` (3000, 8), `stream_koku` (3000, 10),
  `stream_ic` (3000, 2): the encounter stream, in order.
- `cue_goz` (n, 75; colourless), `cue_dokunma`, `cue_kulak`, `cue_koku`: one cue per object seen in the stream.
- `palette` (12, 3).

**`answers_<seed>.npz`** (scoring only): `cue_colour`, `cue_object`, `stream_object`.

## Measure (all pairs)

Answer every object 7 times:

- with all four senses;
- with each pair of senses (6 pairs).

An object is **known** only if all 7 answers are correct. Score it with
`python3 tools/score_hard_dev.py predictions.json`; the file's header describes the predictions format.

## Reference points

Development results on these worlds; they are not locked.

| Learner | Known / seen |
|---|---|
| ERIKA 1, fed from these files (310800–310801) | 280 / 359 (78.0%); identical to the internal run |
| ERIKA 1, internal run, all 6 worlds | 828 / 1074 (77.1%) |
| Store-everything nearest-neighbour reference (internal) | 610 / 1074 (56.8%) |
| Slow memory only (internal) | 353 / 1074 (32.9%) |
| Fast memory only (internal) | 294 / 1074 (27.4%) |
| Neural ERIKA 2, evolved rule (internal, 310800–310801) | 118 / 359 (32.9%) |
