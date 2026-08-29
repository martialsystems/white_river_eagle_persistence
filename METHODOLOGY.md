# Methodology: lag-1 Eagle Creek plus Nora and/or Fall Creek versus Centerton persistence

Question: Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Live science is `ea1c0e1`. Not a yes/no. Eagle-only fails (2,421). Mixes cut peak RMSE (1,607 / 1,668 / 1,694 vs 1,795) and lose the ordinary day (MAE 823 to 938 vs 810). Lead with RMSE ≠ MAE. Three-feature RMSE matches `8e4fdca`. That tree is not restamped. White Lick is a later tree, not a predictor here.

Site lookup first: 03353500 Eagle Creek at Indianapolis, IN, complete. 03353240 79th Street empty: stop, same as 16th Street. 03353451 starts late: stop. No alternate.

Indianapolis is not a feature. OLS is not a pour. Empty or late 00060 stops.

## Layers

| Layer | Role | Source |
|-------|------|--------|
| Feature | lag-1 00060 | NWIS 03353500 Eagle Creek at Indianapolis, IN |
| And/or | lag-1 00060 | NWIS 03351000 White River near Nora, IN |
| And/or | lag-1 00060 | NWIS 03352500 Fall Creek at Millersville, IN |
| Label | 00060 | NWIS 03354000 White River near Centerton, IN |
| Split | same as Eagle gap / Fall Creek / NWM-error | Train through 2018-09-30, hold out 2018-10-01 to 2020-12-31 |

## Figures

1. Holdout hydrograph: Centerton, persistence, Eagle-only, Eagle+Nora+Fall Creek.
2. RMSE bars for the four Eagle mixes versus persistence and cited NWM.

## Claims

Allowed: lag-1 Eagle Creek plus Nora and/or Fall Creek versus Centerton persistence; Eagle-only losing as the control; 03353500 as the official complete record; citing `8e4fdca` and `fa2e315`.

Banned: restamping `8e4fdca`; downloading NWM; calling 03353600 Eagle Creek; inventing a tributary when 00060 is empty or late; HAND as a FIRM; inverting Q to feet; a third figure; treating MAE-worse as a closed reach.
