"""Google Sheets persistence for TeamUp.

Two worksheets in one spreadsheet:
  - Pool   — one row per person who joined
  - Teams  — one row per locked team (member names, JSON)

Lists (skills, availability) are stored pipe-separated so they're readable
in the spreadsheet itself without any JSON noise.

This module is only imported when st.secrets contains [connections.gsheets].
The public API (load_pool, save_pool, load_teams, save_teams) is called by
store.py, which falls back to JSON if this module isn't available.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pandas as pd

from teamup.match import Profile

if TYPE_CHECKING:
    import streamlit as st


_SEP = "|"

_POOL_COLS = [
    "id", "name", "skills", "wants_to_learn",
    "availability", "hours_per_week", "commitment",
]
_TEAMS_COLS = ["team_number", "members_json"]


def _conn(st):
    return st.connection("gsheets", type="sql")  # replaced below — see note


def _get_conn(st):
    """Return a GSheetsConnection. Imported lazily so the module loads fine
    even when st-gsheets-connection isn't installed (JSON path never needs it).
    """
    from streamlit_gsheets import GSheetsConnection  # noqa: PLC0415
    return st.connection("gsheets", type=GSheetsConnection)


# ── encode / decode ──────────────────────────────────────────────────────────

def _enc_list(lst: list) -> str:
    return _SEP.join(lst)


def _dec_list(cell: str) -> list:
    if not cell or (isinstance(cell, float)):
        return []
    return [x.strip() for x in str(cell).split(_SEP) if x.strip()]


def _row_to_profile(row) -> Profile:
    return Profile(
        id=str(row["id"]),
        name=str(row["name"]),
        skills=_dec_list(row["skills"]),
        wants_to_learn=_dec_list(row["wants_to_learn"]),
        availability=_dec_list(row["availability"]),
        hours_per_week=int(row["hours_per_week"]),
        commitment=int(row["commitment"]),
    )


def _profile_to_row(p: Profile) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "skills": _enc_list(p.skills),
        "wants_to_learn": _enc_list(p.wants_to_learn),
        "availability": _enc_list(p.availability),
        "hours_per_week": p.hours_per_week,
        "commitment": p.commitment,
    }


# ── public API ────────────────────────────────────────────────────────────────

def load_pool(st) -> list[Profile]:
    conn = _get_conn(st)
    try:
        df = conn.read(worksheet="Pool", usecols=_POOL_COLS, ttl=0)
        df = df.dropna(subset=["id", "name"])
        return [_row_to_profile(r) for _, r in df.iterrows()]
    except Exception:
        return []


def save_pool(st, pool: list[Profile]) -> None:
    conn = _get_conn(st)
    df = pd.DataFrame([_profile_to_row(p) for p in pool], columns=_POOL_COLS)
    conn.update(worksheet="Pool", data=df)


def load_teams(st) -> list[list[str]]:
    conn = _get_conn(st)
    try:
        df = conn.read(worksheet="Teams", usecols=_TEAMS_COLS, ttl=0)
        df = df.dropna(subset=["members_json"])
        return [json.loads(r["members_json"]) for _, r in df.iterrows()]
    except Exception:
        return []


def save_teams(st, teams: list[list[str]]) -> None:
    conn = _get_conn(st)
    rows = [{"team_number": i + 1, "members_json": json.dumps(t)}
            for i, t in enumerate(teams)]
    df = pd.DataFrame(rows, columns=_TEAMS_COLS)
    conn.update(worksheet="Teams", data=df)
