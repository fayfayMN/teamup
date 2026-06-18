"""Session state + persistence for TeamUp.

Backend is chosen automatically at runtime:
  - Google Sheets  — when st.secrets contains [connections.gsheets]
                     (set up via .streamlit/secrets.toml or Streamlit Cloud secrets)
  - JSON file      — fallback for local dev with no secrets file

All pages call save(st) and init_state(st) — the backend is invisible to them.
"""

from __future__ import annotations

import json
from pathlib import Path

from teamup.match import Profile

_FILE = Path("teamup_state.json")


# ── backend detection ─────────────────────────────────────────────────────────

def _use_sheets(st) -> bool:
    """True when Sheets credentials are present in st.secrets."""
    try:
        return "gsheets" in st.secrets.get("connections", {})
    except Exception:
        return False


# ── JSON backend ──────────────────────────────────────────────────────────────

def _json_load() -> dict | None:
    if not _FILE.exists():
        return None
    try:
        return json.loads(_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _json_save(st) -> None:
    payload = {
        "pool": [p.__dict__.copy() for p in st.session_state.pool],
        "teams_locked": st.session_state.get("teams_locked", []),
    }
    _FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ── public API ────────────────────────────────────────────────────────────────

def save(st) -> None:
    """Persist current pool + locked teams to whichever backend is active."""
    if _use_sheets(st):
        from teamup.gsheets import save_pool, save_teams  # noqa: PLC0415
        save_pool(st, st.session_state.pool)
        save_teams(st, st.session_state.get("teams_locked", []))
    else:
        _json_save(st)


def init_state(st) -> None:
    """Load persisted state into st.session_state on first run of each session."""
    ss = st.session_state
    if ss.get("_inited"):
        return

    if _use_sheets(st):
        from teamup.gsheets import load_pool, load_teams  # noqa: PLC0415
        ss.pool = load_pool(st)
        ss.teams_locked = load_teams(st)
    else:
        saved = _json_load()
        if saved:
            ss.pool = [Profile(**d) for d in saved.get("pool", [])]
            ss.teams_locked = saved.get("teams_locked", [])
        else:
            ss.pool = []
            ss.teams_locked = []

    ss._inited = True


# ── demo data (opt-in only) ───────────────────────────────────────────────────

def demo_pool() -> list[Profile]:
    """8 fictional people for trying the matching flow. Never loaded automatically."""
    return [
        Profile("p1", "Alex", ["Python / coding", "Data / ML"], ["Pitching / presenting"],
                ["Mon evening", "Wed evening", "Sat daytime"], 12, 3),
        Profile("p2", "Sam", ["UI/UX design", "Graphics / branding"], ["Python / coding"],
                ["Mon evening", "Sat daytime"], 8, 3),
        Profile("p3", "Jess", ["Pitching / presenting", "Writing / storytelling"], [],
                ["Wed evening", "Sat daytime"], 6, 2),
        Profile("p4", "Kim", ["Project management", "Market / user research"], [],
                ["Mon evening", "Sat daytime"], 10, 3),
        Profile("p5", "Lee", ["Web / frontend"], ["UI/UX design"],
                ["Tue evening", "Sun daytime"], 5, 1),
        Profile("p6", "Ravi", ["Finance / modeling", "Market / user research"], [],
                ["Tue evening", "Sun daytime"], 7, 2),
        Profile("p7", "Mia", ["Python / coding", "Web / frontend"], ["Data / ML"],
                ["Tue evening", "Sun daytime"], 9, 2),
        Profile("p8", "Tom", ["Graphics / branding"], ["Pitching / presenting"],
                ["Tue evening", "Sun daytime"], 4, 1),
    ]
