# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from ecpers.config import QUESTION
from ecpers.pipeline import stage0_fixture


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["lag1_locked"] is True
    assert report["figures"] == ["hydrograph.png", "rmse_bars.png"]
    assert (tmp_path / "hydrograph.png").is_file()
    assert (tmp_path / "rmse_bars.png").is_file()
    assert report["p_sfha_feature"] is False
    assert report["nwm_citation"] == "fa2e315"
    assert report["eagle_gap_citation"] == "8e4fdca"
