# Glossary: Turkish names in code and raw data

The project's working language is Turkish, so source code and raw output keys are Turkish. This page maps the names
you will meet to English.

## World generator (`world/dunya.py`)

| Name | Meaning |
|---|---|
| `Dunya(seed, ayar)` | a world, built from a seed and settings |
| `DunyaAyar` | world settings |
| `aile` | family: kinds that share a shape and related colours |
| `tur` | kind (hidden; the learner never sees it) |
| `birey`, `bireyler` | individual(s): one object of a kind, with its own fixed colour |
| `renk`, `palet` | colour, colour palette |
| `sekil`, `maske` | shape, shape mask (image) |
| `doku`, `ses` | texture (touch), sound |
| `koku`, `tat` | smell, taste |
| `iz_piksel`, `iz_sapma` | individual mark: number of pixels, size of deviation |
| `akis` | encounter stream (order in which individuals are met) |
| `karsilasma` | encounters (stream length) |
| `emekli`, `emeklilik` | retired: individuals that leave the world early (used for long-term memory) |
| `acilis` | reveal point: when hidden variants start to appear |
| `gizli` | hidden variant: a colour a kind can have but has not shown yet |
| `degisim`, `yeni_kural` | rule change: a kind's colour rule changes mid-stream |
| `test`, `test_birey` | individuals held back for generalisation tests |

## Raw outputs (`records/*/raw/`)

| Name | Meaning |
|---|---|
| `kollar` | arms (systems compared under the same stream) |
| `erika_son_bol_tam_kar_ebk` | the ERIKA system tested in IP0 |
| `epizodik` | reference arm: episodic store only |
| `yavas` | reference arm: slow learner only |
| `denetim` | checkpoints, keyed by encounter number (`"3000"` = end of stream) |
| `tavan` | ceiling: ideal-observer score with the same information |
| `kisa` / `uzun` | short-term / long-term group |
| `ornek_dogruluk` | sample accuracy (scored per sampled recall) |
| `mod_dogruluk` | mode accuracy (most frequent answer per individual) |
| `unutma` (`_son`, `_en_kotu`) | forgetting (final checkpoint, worst checkpoint) |
| `koku_tat.temel` | paired baseline run with taste and smell off |
| `toplu`: `ortalama`, `alt`, `ust`, `en_kotu`, `n` | summary: mean, 95% CI lower, upper, worst world, number of worlds |
| `karar` | decision (PASS / FAIL) |
| `beklenen`, `eksik` | expected worlds, missing worlds |
| `on_kayit` | preregistration |

## Endpoints ↔ raw fields

| Endpoint (`tests/SPEC.md`) | Raw field at checkpoint `"3000"` |
|---|---|
| B1 short-term colour memory | `m10_kisa_ornek_dogruluk` |
| B2 long-term colour memory | `m10_uzun_ornek_dogruluk` |
| B3 shape completion in the dark | `m4_sekil_kisa_tam`, `m4_sekil_uzun_tam` |
| B4 shape of never-seen individuals | `m4_sekil_genel_tam` |
