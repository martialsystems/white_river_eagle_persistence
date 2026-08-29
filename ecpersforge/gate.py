# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from ecpersforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from ecpersforge.graphs.claim_bans import build_graph as build_claims
from ecpersforge.graphs.fetch_nwis import build_graph as build_fetch
from ecpersforge.graphs.no_p_sfha import build_graph as build_p
from ecpersforge.graphs.temporal_split import build_graph as build_split


def require_no_p_sfha(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ecpers_p"))
    state = {"p_sfha_feature": False, "p_sfha_label": False, "p_sfha_figure": False}
    state.update(flags)
    require_law(build_p(), state, allow_decisions=["allow"], law_id="ecpers.no_p_sfha", thread_id=thread_id, raise_error=True)


def require_split(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ecpers_split"))
    state = {"temporal_ok": True, "lag1_locked": True, "indy_predictor": False, "invented_tributary": False}
    state.update(flags)
    require_law(build_split(), state, allow_decisions=["allow"], law_id="ecpers.temporal_split", thread_id=thread_id, raise_error=True)


def require_fetch(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ecpers_fetch"))
    state = {
        "nwis_ok": False,
        "eagle_creek_ok": False,
        "eagle_creek_on_time": False,
        "nwm_repull": False,
        "invented_tributary": False,
    }
    state.update(flags)
    require_law(build_fetch(), state, allow_decisions=["allow"], law_id="ecpers.fetch_nwis", thread_id=thread_id, raise_error=True)


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "ecpers_claims"))
    state = {"lag_as_wet_mask": False, "flood_warning": False, "feet_invert": False, "closed_reach": False, "n_figures": 2}
    state.update(flags)
    require_law(build_claims(), state, allow_decisions=["allow"], law_id="ecpers.claim_bans", thread_id=thread_id, raise_error=True)
