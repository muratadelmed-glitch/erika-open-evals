# Records

One folder per locked evaluation. Each folder has the same files:

| File | What | When written |
|---|---|---|
| `PREREGISTRATION_tr.md` | the binding preregistration: worlds, settings, thresholds, analysis | **before** the run, locked by commit |
| `PREREGISTRATION.md` | English summary (the Turkish file governs if they differ) | after the run, copied unchanged |
| `raw/` | raw outputs of every world, the run manifest and the decision report | by the run |
| `REPORT.md` | results against the preregistered thresholds, met or not | after the run |

## Runs

| Record | What | Result | Re-score it |
|---|---|---|---|
| [`2026-11-IP0/`](2026-11-IP0/) | locked colour-memory exam, 20 unseen evaluation worlds (312001–312020), 3000 encounters each | **PASS** (B1 1.000, B2 1.000; threshold 0.90) | `python3 tools/rescore_ip0.py` |
