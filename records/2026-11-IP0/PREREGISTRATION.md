# IP0 preregistration (English summary)

The binding preregistration is the Turkish original, `PREREGISTRATION_tr.md`. This summary is for convenience only. If the two differ, the Turkish file governs.

- **File SHA-256:** `8f2722df74feb9d70ec30c5b71b0ea3b5944bb072de2258a6bc41050cc073ad1`.
- **Locked** in the private development repository at commit `768595096c53803e41c6ec5e1d484a0698f0f872`, before the run.
  - The lock commit changes only the `statu: KILITLI` line.
  - The run tool refuses to start if the preregistration or the measurement code changed after that commit.
- **Copied here** after the run, unchanged. The SHA-256 matches.

## What is measured

- **System:** the current, probabilistic (non-neural) ERIKA learner, arm `erika_son_bol_tam_kar_ebk`.
- **Reference arms:** an episodic-only arm and a slow-learner-only arm, both under the same stream and the same measurement.
- **Worlds:** 20 never-generated evaluation worlds, seeds 312001–312020.
  - Medium difficulty, with taste and smell.
  - Sharp body (sense noise ÷ 2).
  - 3000 encounters per world.
- **Paired baseline:** taste and smell off, secondary.

## Primary endpoints and decision rule

- **B1:** short-term colour memory.
- **B2:** long-term colour memory, for individuals that already left the world.
- **Cue:** recall is at the end of the stream, from a cue that shows the object's shape with its colour masked (grey image), plus touch, sound and smell. (Corrected 2026-11-23: an earlier version of this summary said the cue had no image; the Turkish original never said that.)
- **PASS:** the 20-world mean is ≥ 0.90 for both B1 and B2. Otherwise **FAIL**.
- **INCONCLUSIVE:** any world missing, crashed or without B1/B2. No rerun.

## Secondary (reported, no threshold)

- Shape completion in the dark (B3, B4).
- Forgetting: final and worst checkpoint (B8).
- Reference arms, the paired baseline, the ideal-observer ceiling, a bootstrap 95% interval (10,000 resamples, seed 0) and the worst world.
