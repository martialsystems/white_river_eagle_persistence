# Agent notes: white_river_eagle_persistence

Public GitHub. MIT. Question: Does lag-1 Eagle Creek (plus Nora and/or Fall Creek) beat Centerton persistence on the same WY2019 to 2020 split?

Eagle-only loses (2,421 vs 1,795). Mixes beat RMSE, not MAE. Three-feature 1,607 matches `8e4fdca`.

Site lookup first: 03353500. 03353240 empty: stop, same as 16th Street. 03353451 starts late: stop. No alternate.

Do not restamp Eagle gap `8e4fdca`, Fall Creek `962d503` / `ccdf4ac`, or NWM `fa2e315`. Do not download NWM. Indianapolis not in X. Hydrology gist only. No sixth raster.

`ecpersforge/` GraphForge pin: no `p_sfha`, lag-1 locked, Eagle Creek 00060 fetch-or-stop (empty or late), no invented tributary, no NWM download.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
