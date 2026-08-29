# Copyright (c) 2026 Martial Systems LLC
"""Lag-1 Eagle Creek plus Nora and/or Fall Creek vs Centerton persistence. No p_sfha. No NWM download."""

from __future__ import annotations

from datetime import date

QUESTION = "Does adding Eagle Creek help you guess tomorrow's flow at Centerton?"

NORA_ID = "03351000"
NORA_NAME = "WHITE RIVER NEAR NORA, IN"
FALL_CREEK_ID = "03352500"
FALL_CREEK_NAME = "FALL CREEK AT MILLERSVILLE, IN"
EAGLE_CREEK_ID = "03353500"
EAGLE_CREEK_NAME = "EAGLE CREEK AT INDIANAPOLIS, IN"
CENTERTON_ID = "03354000"
CENTERTON_NAME = "WHITE RIVER NEAR CENTERTON, IN"
INDY_ID = "03353000"
LITTLE_EAGLE_ID = "03353600"
ZIONSVILLE_ID = "03353200"
BELOW_RESERVOIR_ID = "03353451"
SEVENTYNINTH_ID = "03353240"
CLERMONT_ID = "03353460"

LAG_DAYS = 1
MAX_FIGURES = 2
LIVE_START = date(2016, 10, 1)
LIVE_END = date(2020, 12, 31)
TRAIN_END = date(2018, 9, 30)
HOLDOUT_START = date(2018, 10, 1)

ANDERSON_NORA_CITATION = "58859be"
FALL_CREEK_CITATION = "962d503"
EAGLE_GAP_CITATION = "8e4fdca"
EAGLE_GAP_THREE_RMSE_CFS = 1607.31
NWM_CITATION = "fa2e315"
NWM_CENTERTON_RMSE_CFS = 2414.32
NWM_CENTERTON_PERS_RMSE_CFS = 1794.57

LOCKED_LIVE_COMMIT = "ea1c0e1"
USER_AGENT = "MartialSystemsResearch/white_river_eagle_persistence"
NWIS_DV_URL = (
    "https://waterservices.usgs.gov/nwis/dv/?format=json&sites={site}"
    "&startDT={start}&endDT={end}&parameterCd=00060&siteStatus=all"
)
