# Agent notes: white_river_eagle_persistence

Public GitHub. MIT. Question: Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Science lock: `ea1c0e1`. Not a yes/no. Eagle-only fails (2,421). Mixes cut peak RMSE (1,607 / 1,668 / 1,694 vs 1,795) and lose MAE (823 to 938 vs 810). Lead with RMSE ≠ MAE. Do not re-fit.

Site: 03353500 Eagle Creek at Indianapolis, IN. 03353240 empty: stop, same as 16th Street. 03353451 starts late: stop. No alternate. No 2026. No `p_sfha`.

Do not restamp `8e4fdca`, Fall Creek `962d503`, or NWM `fa2e315`. Do not download NWM. Indianapolis not in X. White Lick is a later tree, not a third predictor here. Hydrology gist only, not gist 1.

Sibling links in the README: fall_creek_gap, nwm_error, hydrology gist.

`ecpersforge/` GraphForge pin: no `p_sfha`, lag-1 locked, Eagle Creek 00060 fetch-or-stop (empty or late), no invented tributary, no NWM download.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
