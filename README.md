# White River Eagle Creek vs Centerton persistence

Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Eagle-only: no. Mixes: yes on RMSE, no on MAE. Live skill is in `logs/nora_live/`.

Holdout RMSE: Eagle-only **2,421** loses to Centerton lag 1 d **1,795**. That is the control, the same honesty as Nora-only losing to Indianapolis persistence: Eagle Creek by itself is not the nowcast. Eagle plus Nora **1,668**, Eagle plus Fall Creek **1,694**, and Eagle plus both **1,607** beat 1,795. Cited NWM **2,414**. Three-feature 1,607 matches locked `8e4fdca` on this same 00060 matrix. That tree asked versus Nora-plus-Fall-Creek (1,734) and is not restamped.

MAE never beats persistence: Eagle-only 1,558, Eagle+Nora 872, Eagle+FC 938, three-feature 823, versus Centerton lag 1 d **810**. RMSE mixes win; typical error does not. White Lick is still open.

Site lookup first: **03353500** EAGLE CREEK AT INDIANAPOLIS, IN. Complete daily 00060 on 2016-10-01 to 2020-12-31 (1,553 / 1,553). **03353240** EAGLE CREEK AT 79TH STREET AT INDIANAPOLIS, IN is empty on this window: stop, same as Fall Creek 16th Street. **03353451** EAGLE CREEK BELOW RESERVOIR AT INDIANAPOLIS, IN starts 2016-10-26: stop. **03353200** Zionsville has three gaps. **03353460** Clermont is complete but not the mouth-ward gage. **03353600** LITTLE EAGLE CREEK is a different creek. Empty or late 03353500 00060 stops. No alternate.

Indianapolis 03353000 is not a feature. OLS weight 7.10 on Eagle-only is not a pour. Daily 00060. No 2026. This tree does not read `p_sfha` and does not paint HAND. Cite Fall Creek `962d503` and NWM `fa2e315`. Do not download NWM.

![Figure 1. Holdout hydrograph at Centerton](logs/nora_live/hydrograph.png)

Figure 1. Centerton 00060, Centerton lag 1 d, Eagle Creek lag 1 d, Eagle plus Nora plus Fall Creek. cfs. Eagle-only overshoots. 1,607 beats 1,795 on RMSE.

![Figure 2. RMSE vs persistence](logs/nora_live/rmse_bars.png)

Figure 2. Holdout RMSE. Eagle-only loses to persistence. Mixes beat it. Cited NWM is `fa2e315`, not downloaded.

## What was compared

| USGS site | Official name | Role |
|-----------|---------------|------|
| 03353500 | EAGLE CREEK AT INDIANAPOLIS, IN | Required feature: lag-1 **00060** |
| 03351000 | WHITE RIVER NEAR NORA, IN | And/or feature: lag-1 **00060** |
| 03352500 | FALL CREEK AT MILLERSVILLE, IN | And/or feature: lag-1 **00060** |
| 03354000 | WHITE RIVER NEAR CENTERTON, IN | Label. Persistence bar is this gage lag 1 d. |

Lag locked at 1 d. Train-only OLS. Holdout 2018-10-01 to 2020-12-31.

## Live skill (holdout 2018-10-01 to 2020-12-31)

| Predictor of Centerton 00060 on day t | RMSE (cfs) | MAE (cfs) | Beats persistence RMSE |
|---------------------------------------|-----------:|----------:|:----------------------:|
| Eagle + Nora + Fall Creek lag 1 d | 1,607 | 823 | yes |
| Eagle + Nora lag 1 d | 1,668 | 872 | yes |
| Eagle + Fall Creek lag 1 d | 1,694 | 938 | yes |
| Centerton 00060 lag 1 calendar day | 1,795 | 810 | bar |
| NWM v2.1 at Centerton (cited fa2e315) | 2,414 | n/a | no |
| Eagle Creek lag 1 d only | 2,421 | 1,558 | no |

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
