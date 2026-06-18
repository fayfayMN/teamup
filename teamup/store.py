"""Session + JSON-file state for TeamUp (same persistence pattern as Clearwork)."""

from __future__ import annotations

import json
from pathlib import Path

from teamup.match import Profile

_FILE = Path("teamup_state.json")


def _profile_to_dict(p: Profile) -> dict:
    return p.__dict__.copy()


def save(st) -> None:
    payload = {
        "pool": [_profile_to_dict(p) for p in st.session_state.pool],
        "teams_locked": st.session_state.get("teams_locked", []),
    }
    _FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _load() -> dict | None:
    if not _FILE.exists():
        return None
    try:
        return json.loads(_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def init_state(st) -> None:
    ss = st.session_state
    if ss.get("_inited"):
        return

    saved = _load()
    if saved:
        ss.pool = [Profile(**d) for d in saved.get("pool", [])]
        ss.teams_locked = saved.get("teams_locked", [])
    else:
        ss.pool = _demo_pool()
        ss.teams_locked = []
    ss._inited = True


def _demo_pool():
    return [
        Profile("p1", "Alex", ["Python / coding", "Data / ML"], ["Pitching / presenting"],
                ["mon-eve", "wed-eve", "sat-day"], 12, 3),
        Profile("p2", "Sam", ["UI/UX design", "Graphics / branding"], ["Python / coding"],
                ["mon-eve", "sat-day"], 8, 3),
        Profile("p3", "Jess", ["Pitching / presenting", "Writing / storytelling"], [],
                ["wed-eve", "sat-day"], 6, 2),
        Profile("p4", "Kim", ["Project management", "Market / user research"], [],
                ["mon-eve", "sat-day"], 10, 3),
        Profile("p5", "Lee", ["Web / frontend"], ["UI/UX design"],
                ["tue-eve", "sun-day"], 5, 1),
        Profile("p6", "Ravi", ["Finance / modeling", "Market / user research"], [],
                ["tue-eve", "sun-day"], 7, 2),
        Profile("p7", "Mia", ["Python / coding", "Web / frontend"], ["Data / ML"],
                ["tue-eve", "sun-day"], 9, 2),
        Profile("p8", "Tom", ["Graphics / branding"], ["Pitching / presenting"],
                ["tue-eve", "sun-day"], 4, 1),
    ]
