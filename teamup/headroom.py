"""Headroom context compression integration for TeamUp.

Headroom (https://github.com/headroomlabs-ai/headroom) is a local compression
layer that cuts LLM context tokens by 47-92%. This module is a PLACEHOLDER —
TeamUp is fully key-less today (matching is pure Python, no LLM calls).

When LLM features land in v4 (plan.md), this module is the integration point.
Until then it renders an informational sidebar section and provides safe
passthrough wrappers that any future code can call without checking for
installation first.

Usage (future):
    from teamup.headroom import compress_messages, is_available

    if is_available():
        messages = compress_messages(messages)
    # else: messages are used as-is (fail-open)
"""

from __future__ import annotations

_available: bool | None = None
_compress_fn = None


def is_available() -> bool:
    """Check if Headroom is installed and importable. Cached after first call."""
    global _available, _compress_fn
    if _available is not None:
        return _available
    try:
        from headroom import compress as _c
        _compress_fn = _c
        _available = True
    except ImportError:
        _available = False
        _compress_fn = False  # sentinel: tried and failed
    return _available


def compress_messages(messages: list, model: str = "gpt-4o") -> list:
    """Compress a message list. Returns the compressed list, or the original on
    any failure (fail-open — the LLM call must never break because compression
    failed)."""
    if not is_available() or not _compress_fn:
        return messages
    try:
        result = _compress_fn(messages, model=model)
        return list(result.messages)
    except Exception:
        return messages


def show_sidebar_controls(st) -> None:
    """Render Headroom controls in the sidebar. Safe to call at any time —
    shows an informational message when headroom is not installed, and
    functional controls when it is."""
    st.divider()
    st.subheader("🗜️ Context compression")
    st.caption(
        "For future LLM features (v4). Install with: "
        "`pip install \"headroom-ai[ml]\"` (~500 MB one-time model download)."
    )

    st.session_state.setdefault("headroom_enabled", False)
    st.session_state.setdefault("headroom_mode", "library")

    if not is_available():
        st.info(
            "Headroom is not installed. LLM features (coming in v4) will work "
            "without compression. To enable compression later: "
            "`pip install \"headroom-ai[ml]\"`"
        )
        return

    st.session_state.headroom_enabled = st.checkbox(
        "Enable Headroom compression",
        value=st.session_state.headroom_enabled,
        help="Compresses context before sending to LLM. Requires Headroom "
             "to be installed.",
        disabled=True,  # No LLM features yet
    )
    st.caption("(LLM features coming in v4 — compression will activate then)")
