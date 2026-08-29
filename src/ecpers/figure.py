# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ecpers.claims import require_clean
from ecpers.config import MAX_FIGURES
from ecpers.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_hydrograph(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ho = fit["holdout"]
    dates = [datetime.strptime(str(x)[:10], "%Y-%m-%d") for x in ho["dates"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(dates, ho["centerton_cfs"], color="#222222", lw=1.4, label="Centerton 00060")
    ax.plot(dates, ho["persistence_cfs"], color="#7a7a7a", lw=1.0, ls="--", label="Centerton 00060 lag 1 d")
    ax.plot(dates, ho["eagle_cfs"], color="#b36b00", lw=1.1, label="Eagle Creek lag 1 d")
    ax.plot(
        dates,
        ho["eagle_nora_fall_creek_cfs"],
        color="#1b6ca8",
        lw=1.2,
        label="Eagle + Nora + Fall Creek",
    )
    ax.set_ylabel("USGS daily mean 00060 (cfs)")
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.12, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_bars(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    skill = fit["skill"]
    keys = [
        ("eagle_nora_fall_creek", "Eagle+Nora+FC"),
        ("eagle_nora", "Eagle+Nora"),
        ("eagle_fall_creek", "Eagle+FC"),
        ("eagle", "Eagle only"),
        ("persistence_target", "Centerton lag 1 d"),
        ("nwm_cited", "NWM cited"),
    ]
    labels = [k[1] for k in keys]
    vals = [skill[k[0]]["rmse_cfs"] for k in keys]
    colors = ["#1b6ca8", "#3d8fbf", "#6aa9c9", "#b36b00", "#7a7a7a", "#555555"]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Holdout RMSE (cfs)")
    ax.set_title(title, fontsize=10)
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.18, top=0.88, left=0.12, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any]) -> list[Path]:
    pers = fit["skill"]["persistence_target"]["rmse_cfs"]
    paths = [
        write_hydrograph(
            log_dir / "hydrograph.png",
            fit=fit,
            title="Centerton holdout: USGS daily mean 00060",
            subtitle="Observed Centerton, lag 1 d, Eagle Creek lag 1 d, Eagle+Nora+Fall Creek. cfs.",
        ),
        write_bars(
            log_dir / "rmse_bars.png",
            fit=fit,
            title="Holdout RMSE vs Centerton persistence",
            subtitle=f"Persistence {pers:.0f} cfs. Cited NWM is fa2e315, not downloaded. OLS, not a pour.",
        ),
    ]
    _cap(len(paths))
    return paths
