# White River Eagle Creek vs Centerton persistence

Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Eagle-only: no. Mixes: yes on RMSE, no on MAE. Science lock: `ea1c0e1`.

The bar is Centerton 00060 from the previous calendar day (03354000). If lag-1 Eagle Creek alone beat that bar, the tributary would be a nowcast of the stem. It does not. Eagle-only RMSE is **2,421** against persistence **1,795**. That is the same control as Nora-only losing to Indianapolis persistence: the named creek by itself is not the river.

Nora and Fall Creek are the and/or companions. Put either one with Eagle Creek, or put both, and RMSE falls below 1,795: Eagle plus Nora **1,668**, Eagle plus Fall Creek **1,694**, Eagle plus both **1,607**. Those three mixes beat persistence on squared error. They do not beat it on typical error. MAE stays above persistence **810** for every mix (823, 872, 938). Persistence still wins the usual day. The RMSE win is peaks. White Lick is still open.

The 1,607 three-feature RMSE matches locked `8e4fdca` on this same 00060 matrix. That tree asked a different question (versus Nora-plus-Fall-Creek **1,734**, MAE 823 vs 791) and is not restamped. Cited NWM at Centerton is **2,414** (`fa2e315`, not downloaded). Fall Creek Indianapolis 1,265 is `962d503`.

![Figure 1. Holdout hydrograph at Centerton](logs/nora_live/hydrograph.png)

Figure 1. Observed Centerton 00060, Centerton lag 1 d, Eagle Creek lag 1 d, and Eagle plus Nora plus Fall Creek. cfs. Eagle-only overshoots because a single OLS weight (7.10) is being asked to stand in for the whole stem. That weight is not a pour of Eagle Creek into White River.

![Figure 2. RMSE vs persistence](logs/nora_live/rmse_bars.png)

Figure 2. Holdout RMSE. Eagle-only is worse than persistence and about even with cited NWM. Mixes that include Nora and/or Fall Creek sit below the persistence bar.

## What was compared

Lag-1 daily mean 00060, train-only OLS, holdout 2018-10-01 to 2020-12-31. Indianapolis 03353000 is not a feature. This tree does not read `p_sfha` and does not paint HAND. Daily 00060, not feet. No 2026.

| USGS site | Name | Role |
|-----------|------|------|
| 03353500 | Eagle Creek at Indianapolis, IN | Required feature: lag-1 **00060** |
| 03351000 | White River near Nora, IN | And/or feature: lag-1 **00060** |
| 03352500 | Fall Creek at Millersville, IN | And/or feature: lag-1 **00060** |
| 03354000 | White River near Centerton, IN | Label. Persistence bar is this gage lag 1 d. |

Site lookup first. **03353500** Eagle Creek at Indianapolis, IN has a complete daily 00060 on 2016-10-01 to 2020-12-31 (1,553 / 1,553). Empty or late 00060 at that site is a stop. No alternate.

| Looked up, not used | Why |
|---------------------|-----|
| 03353240 Eagle Creek at 79th Street at Indianapolis, IN | Empty 00060 on this window. Stop, same as Fall Creek 16th Street. |
| 03353451 Eagle Creek below reservoir at Indianapolis, IN | Starts 2016-10-26. Late. Stop. |
| 03353200 Eagle Creek at Zionsville, IN | Three gaps. |
| 03353460 Eagle Creek at Clermont, IN | Complete, but not the mouth-ward gage. |
| 03353600 Little Eagle Creek at Speedway, IN | A different creek. |

## Live skill (holdout 2018-10-01 to 2020-12-31)

Read RMSE against the 1,795 bar, then MAE against the 810 bar. A yes in the last column is squared error only.

| Predictor of Centerton 00060 on day t | RMSE (cfs) | MAE (cfs) | Beats persistence RMSE |
|---------------------------------------|-----------:|----------:|:----------------------:|
| Eagle + Nora + Fall Creek lag 1 d | 1,607 | 823 | yes |
| Eagle + Nora lag 1 d | 1,668 | 872 | yes |
| Eagle + Fall Creek lag 1 d | 1,694 | 938 | yes |
| Centerton 00060 lag 1 calendar day | 1,795 | 810 | bar |
| NWM v2.1 at Centerton (cited fa2e315) | 2,414 | n/a | no |
| Eagle Creek lag 1 d only | 2,421 | 1,558 | no |

## Stage 0

Synthetic Nora plus Fall Creek plus an independent Eagle Creek pulse so CI recovers an Eagle Creek coefficient without NWIS. Fixture under `logs/stage0_fixture/`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```

Two figures max. Empty or late Eagle Creek 00060 stops (`run_live.py` exit 2).
