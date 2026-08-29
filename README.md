# White River Eagle Creek vs Centerton persistence

Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Not a yes/no. Eagle-only fails. Mixes cut peak error and lose the ordinary day. Science lock: `ea1c0e1`.

**1,607 / 1,668 / 1,694** vs persistence **1,795** RMSE is a real peak win. MAE **823 to 938** vs **810** means Centerton lag 1 d still wins the ordinary day. Eagle-only **2,421** is a no: weight 7.10 is not the stem. Cited NWM **2,414** stays last.

That matches Fall Creek at Indianapolis only in part. There the mix also beat the target's persistence on the number we led with (1,265 vs 1,450, `962d503`). Here RMSE and MAE disagree, so the lead is RMSE ≠ MAE. The three-feature RMSE 1,607 matches `8e4fdca` on this matrix. That tree asked versus Nora-plus-Fall-Creek (1,734) and is not restamped.

Site **03353500** Eagle Creek at Indianapolis, IN. Same split as NWM-error and Fall Creek: train through 2018-09-30, hold out 2018-10-01 to 2020-12-31. No 2026. This tree does not read `p_sfha`. Daily 00060, cfs, not feet. Indianapolis 03353000 is not a feature.

![Figure 1. Holdout hydrograph at Centerton](logs/nora_live/hydrograph.png)

Figure 1. Centerton 00060, Centerton lag 1 d, Eagle Creek lag 1 d, Eagle plus Nora plus Fall Creek. Eagle-only overshoots. Weight 7.10 is OLS, not a pour.

![Figure 2. RMSE vs persistence](logs/nora_live/rmse_bars.png)

Figure 2. Holdout RMSE. Mixes sit below persistence. Eagle-only sits with cited NWM at the back.

## What was compared

Lag-1 daily mean 00060, train-only OLS.

| USGS site | Name | Role |
|-----------|------|------|
| 03353500 | Eagle Creek at Indianapolis, IN | Required feature: lag-1 **00060** |
| 03351000 | White River near Nora, IN | And/or feature: lag-1 **00060** |
| 03352500 | Fall Creek at Millersville, IN | And/or feature: lag-1 **00060** |
| 03354000 | White River near Centerton, IN | Label. Persistence bar is this gage lag 1 d. |

Site lookup first. **03353500** has a complete daily 00060 on 2016-10-01 to 2020-12-31 (1,553 / 1,553). Empty or late 00060 at that site is a stop. No alternate.

| Looked up, not used | Why |
|---------------------|-----|
| 03353240 Eagle Creek at 79th Street at Indianapolis, IN | Empty 00060 on this window. Stop, same as Fall Creek 16th Street. |
| 03353451 Eagle Creek below reservoir at Indianapolis, IN | Starts 2016-10-26. Late. Stop. |
| 03353200 Eagle Creek at Zionsville, IN | Three gaps. |
| 03353460 Eagle Creek at Clermont, IN | Complete, but not the mouth-ward gage. |
| 03353600 Little Eagle Creek at Speedway, IN | A different creek. |

## Live skill (holdout 2018-10-01 to 2020-12-31)

RMSE against the 1,795 bar, MAE against the 810 bar. Those two columns are not the same ranking.

| Predictor of Centerton 00060 on day t | RMSE (cfs) | MAE (cfs) |
|---------------------------------------|-----------:|----------:|
| Eagle + Nora + Fall Creek lag 1 d | 1,607 | 823 |
| Eagle + Nora lag 1 d | 1,668 | 872 |
| Eagle + Fall Creek lag 1 d | 1,694 | 938 |
| Centerton 00060 lag 1 calendar day | 1,795 | 810 |
| NWM v2.1 at Centerton (cited fa2e315) | 2,414 | n/a |
| Eagle Creek lag 1 d only | 2,421 | 1,558 |

White Lick is a later tree if the next named lateral is worth a night. It is not a third predictor in this fit.

## Siblings

- Fall Creek gap: https://github.com/martialsystems/white_river_fall_creek_gap (`962d503`)
- NWM error: https://github.com/martialsystems/white_river_nwm_error (`fa2e315`)
- Hydrology gist: https://gist.github.com/martialsystems/1104e5e47b8a04006ec694d289d43639

## Stage 0

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```

Two figures max. Empty or late Eagle Creek 00060 stops (`run_live.py` exit 2).
