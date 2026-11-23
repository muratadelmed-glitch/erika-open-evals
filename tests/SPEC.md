# Memory test specification (draft)

All tests read the learner only through two calls: *complete the colour of this object from these senses* and
*complete the missing sense of this object*. Measurement never feeds back into learning.

| Id | Name | What | Score | Reference levels |
|---|---|---|---|---|
| B1 | Short-term memory | colour of individuals seen in the last 150 encounters, cued by colourless sight + touch + sound (+ smell) | sample accuracy | chance 1/12; ideal-observer ceiling reported |
| B2 | Long-term memory | colour of "retired" individuals seen only early in the stream | sample accuracy | as B1 |
| B3 | Completion in the dark | shape of an individual from touch + sound only | exact-shape rate | ceiling reported |
| B4 | Generalisation | shape of never-seen individuals of known kinds | exact-shape rate | learning ideal reported |
| B5 | Protection after a rule change | colour of old individuals of a kind whose colour rule changed | sample accuracy | — |
| B6 | Adaptation | share of the new colour rule for never-seen members after the change | share | descriptive |
| B8 | Forgetting | individuals once recalled correctly (mode) that are later wrong; final point and worst point (temporary loss counts) | fraction | target ≤ 0.1–0.2 % |

The statistical unit is the world: world mean, 95 % bootstrap interval over worlds, and the worst world are
reported. Exact thresholds for a locked run live in its pre-registration under `records/`.

Status: the reference implementation of these measurements runs inside the private repository because it needs the
digital body to generate the cues. For outside use, pre-computed sensory streams and cues for 10 development worlds are in `data/ip0-dev/`.
