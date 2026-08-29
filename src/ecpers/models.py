# Copyright (c) 2026 Martial Systems LLC
"""Lag-1 Eagle Creek with Nora and/or Fall Creek. Bar is Centerton persistence. Lag frozen at 1."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import LinearRegression

from ecpers.config import (
    BELOW_RESERVOIR_ID,
    CENTERTON_ID,
    CLERMONT_ID,
    EAGLE_CREEK_ID,
    FALL_CREEK_ID,
    INDY_ID,
    LAG_DAYS,
    LITTLE_EAGLE_ID,
    NORA_ID,
    NWM_CENTERTON_RMSE_CFS,
    NWM_CITATION,
    SEVENTYNINTH_ID,
    ZIONSVILLE_ID,
)
from ecpers.errors import LeakError, SplitError
from ecpers.pack import QPack
from ecpers.split import assert_temporal, temporal_masks


def rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float)
    ok = np.isfinite(e)
    return float(np.sqrt(np.mean(e[ok] * e[ok]))) if ok.any() else float("nan")


def mae(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.abs(np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float))
    ok = np.isfinite(e)
    return float(np.mean(e[ok])) if ok.any() else float("nan")


def _lag(arr: np.ndarray, k: int) -> np.ndarray:
    if k < 0:
        raise SplitError("negative lag is a future leak")
    src = np.asarray(arr, dtype=float)
    if k == 0:
        return src.copy()
    out = np.full(arr.shape, np.nan, dtype=float)
    out[k:] = src[:-k]
    return out


def _fit_cols(x: np.ndarray, y: np.ndarray, train: np.ndarray, hold: np.ndarray) -> tuple[np.ndarray, LinearRegression]:
    lr = LinearRegression()
    lr.fit(x[train], y[train])
    return lr.predict(x[hold]), lr


def _skill_row(y: np.ndarray, yhat: np.ndarray, lr: LinearRegression, names: tuple[str, ...]) -> dict[str, Any]:
    row: dict[str, Any] = {
        "rmse_cfs": rmse(y, yhat),
        "mae_cfs": mae(y, yhat),
        "intercept": float(lr.intercept_),
        "lag_days": LAG_DAYS,
        "beats_persistence_rmse": None,
    }
    for name, coef in zip(names, lr.coef_):
        row[f"coef_{name}"] = float(coef)
    return row


def fit_pack(pack: QPack) -> dict[str, Any]:
    nora = np.asarray(pack.nora_cfs, dtype=float)
    fc = np.asarray(pack.fall_creek_cfs, dtype=float)
    eagle = np.asarray(pack.eagle_creek_cfs, dtype=float)
    cent = np.asarray(pack.centerton_cfs, dtype=float)
    train_all, hold_all = temporal_masks(pack.dates)
    assert_temporal(pack.dates, train_all, hold_all)
    nora_l1 = _lag(nora, LAG_DAYS)
    fc_l1 = _lag(fc, LAG_DAYS)
    eagle_l1 = _lag(eagle, LAG_DAYS)
    pers = _lag(cent, LAG_DAYS)
    if LAG_DAYS != 1:
        raise SplitError("lag is locked at 1 calendar day")
    ok = (
        np.isfinite(nora_l1)
        & np.isfinite(fc_l1)
        & np.isfinite(eagle_l1)
        & np.isfinite(cent)
        & np.isfinite(pers)
    )
    train, hold = train_all & ok, hold_all & ok
    if not train.any() or not hold.any():
        raise SplitError("no valid rows after lag")
    y_ho, pers_ho = cent[hold], pers[hold]
    specs = (
        ("eagle", (eagle_l1,), ("eagle_creek",)),
        ("eagle_nora", (eagle_l1, nora_l1), ("eagle_creek", "nora")),
        ("eagle_fall_creek", (eagle_l1, fc_l1), ("eagle_creek", "fall_creek")),
        ("eagle_nora_fall_creek", (eagle_l1, nora_l1, fc_l1), ("eagle_creek", "nora", "fall_creek")),
    )
    skill: dict[str, Any] = {
        "persistence_target": {"rmse_cfs": rmse(y_ho, pers_ho), "mae_cfs": mae(y_ho, pers_ho)},
        "nwm_cited": {"rmse_cfs": NWM_CENTERTON_RMSE_CFS, "source": NWM_CITATION},
    }
    hats: dict[str, np.ndarray] = {}
    pers_rmse = skill["persistence_target"]["rmse_cfs"]
    pers_mae = skill["persistence_target"]["mae_cfs"]
    beats_rmse: list[str] = []
    beats_mae: list[str] = []
    for key, cols, names in specs:
        x = np.column_stack(cols)
        yhat, lr = _fit_cols(x, cent, train, hold)
        hats[key] = yhat
        row = _skill_row(y_ho, yhat, lr, names)
        row["beats_persistence_rmse"] = bool(row["rmse_cfs"] < pers_rmse)
        row["beats_persistence_mae"] = bool(row["mae_cfs"] < pers_mae)
        skill[key] = row
        if row["beats_persistence_rmse"]:
            beats_rmse.append(key)
        if row["beats_persistence_mae"]:
            beats_mae.append(key)
    if "eagle_nora_fall_creek" in beats_rmse and "eagle" in beats_rmse:
        verdict = "eagle_alone_and_with_companions_beat_persistence_rmse"
    elif beats_rmse:
        verdict = "some_eagle_mixes_beat_persistence_rmse"
    else:
        verdict = "persistence_holds"
    return {
        "lag_days": LAG_DAYS,
        "lag1_locked": True,
        "skill": skill,
        "verdict": verdict,
        "beats_persistence_rmse": beats_rmse,
        "beats_persistence_mae": beats_mae,
        "predictor_sites": [EAGLE_CREEK_ID, NORA_ID, FALL_CREEK_ID],
        "label_sites": [CENTERTON_ID],
        "holdout": {
            "dates": pack.dates[hold],
            "centerton_cfs": y_ho,
            "persistence_cfs": pers_ho,
            "eagle_cfs": hats["eagle"],
            "eagle_nora_cfs": hats["eagle_nora"],
            "eagle_fall_creek_cfs": hats["eagle_fall_creek"],
            "eagle_nora_fall_creek_cfs": hats["eagle_nora_fall_creek"],
        },
    }


def assert_features_clean(fit: dict[str, Any]) -> None:
    preds = list(fit.get("predictor_sites") or [])
    banned = {
        INDY_ID,
        CENTERTON_ID,
        LITTLE_EAGLE_ID,
        ZIONSVILLE_ID,
        BELOW_RESERVOIR_ID,
        SEVENTYNINTH_ID,
        CLERMONT_ID,
    }
    hit = banned.intersection(preds)
    if hit:
        raise LeakError(f"banned site in X: {sorted(hit)}")
    if EAGLE_CREEK_ID not in preds:
        raise LeakError("Eagle Creek Indianapolis must be a feature")
    if fit.get("lag_days") != 1 or not fit.get("lag1_locked"):
        raise SplitError("lag is locked at 1 calendar day")
