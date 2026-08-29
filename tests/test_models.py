# Copyright (c) 2026 Martial Systems LLC

import json
from pathlib import Path

from ecpers.config import (
    CENTERTON_ID,
    EAGLE_CREEK_ID,
    EAGLE_GAP_THREE_RMSE_CFS,
    FALL_CREEK_ID,
    INDY_ID,
    LITTLE_EAGLE_ID,
    NORA_ID,
    NWM_CENTERTON_PERS_RMSE_CFS,
    SEVENTYNINTH_ID,
)
from ecpers.errors import LeakError
from ecpers.fixture import build_fixture
from ecpers.models import assert_features_clean, fit_pack

LIVE_REPORT = Path(__file__).resolve().parents[1] / "logs" / "nora_live" / "stage_c_report.json"


def test_fixture_eagle_mixes_beat_persistence() -> None:
    fit = fit_pack(build_fixture())
    assert fit["lag_days"] == 1
    assert EAGLE_CREEK_ID in fit["predictor_sites"]
    assert INDY_ID not in fit["predictor_sites"]
    assert CENTERTON_ID not in fit["predictor_sites"]
    assert LITTLE_EAGLE_ID not in fit["predictor_sites"]
    assert SEVENTYNINTH_ID not in fit["predictor_sites"]
    assert_features_clean(fit)
    skill = fit["skill"]
    pers = skill["persistence_target"]["rmse_cfs"]
    assert skill["eagle_nora_fall_creek"]["rmse_cfs"] < pers
    assert skill["eagle"]["coef_eagle_creek"] != 0
    assert skill["nwm_cited"]["source"] == "fa2e315"
    dirty = dict(fit)
    dirty["predictor_sites"] = [EAGLE_CREEK_ID, NORA_ID, FALL_CREEK_ID, INDY_ID]
    try:
        assert_features_clean(dirty)
        raise AssertionError("expected leak")
    except LeakError:
        pass


def test_live_three_feature_and_persistence_match_citations() -> None:
    if not LIVE_REPORT.is_file():
        return
    report = json.loads(LIVE_REPORT.read_text(encoding="utf-8"))
    three = report["skill"]["eagle_nora_fall_creek"]["rmse_cfs"]
    pers = report["skill"]["persistence_target"]["rmse_cfs"]
    assert abs(three - EAGLE_GAP_THREE_RMSE_CFS) < 0.05
    assert abs(pers - NWM_CENTERTON_PERS_RMSE_CFS) < 0.05
    assert report["nwm_citation"] == "fa2e315"
    assert report["eagle_gap_citation"] == "8e4fdca"
