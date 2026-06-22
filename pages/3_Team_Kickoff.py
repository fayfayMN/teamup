"""Team Kickoff — the differentiator. A guided 30-minute launch that outputs a
working agreement. This is where most matching tools stop and most teams fail."""

import streamlit as st

from teamup.store import init_state

st.set_page_config(page_title="Team Kickoff · TeamUp", page_icon="🚀", layout="wide")
init_state(st)

st.title("🚀 Team Kickoff")
st.caption("Spend the first 30 minutes on people, not ideas. This produces a working "
           "agreement the whole team signs off on — your defense against free riders "
           "and credit-takers later.")

# One-click demo fill: populates the team name + domain owners so you can show a
# complete working agreement instantly. (The rules below come pre-filled already.)
_EXAMPLE = {
    "kick_team": "HackMAC 2026",
    "own_Build": "Mia", "own_Design": "Sam", "own_Pitch": "Jess",
    "own_Organize": "Kim", "own_Integrator (watches the whole picture)": "Alex",
}
if st.button("✨ Fill with an example team"):
    for _k, _v in _EXAMPLE.items():
        st.session_state[_k] = _v
    st.rerun()

team_name = st.text_input("Team / project name", key="kick_team",
                          placeholder="e.g. HackMAC 2026")

st.markdown("#### 1. Domain owners (one per area — not a leader for everything)")
ROLES = ["Build", "Design", "Pitch", "Organize", "Integrator (watches the whole picture)"]
owners = {}
for r in ROLES:
    owners[r] = st.text_input(r, key=f"own_{r}", placeholder="who owns this?")

st.markdown("#### 2. Decision rule")
decision = st.text_input(
    "When stuck, how do we decide?",
    value="The domain owner decides after 10 minutes of disagreement, and we move on.",
)

st.markdown("#### 3. Check-ins")
checkins = st.text_input("When do we sync?",
                         value="At the midpoint and 2 hours before the deadline.")

st.markdown("#### 4. If someone goes quiet")
quiet = st.text_input(
    "Our rule:",
    value="We ask what's blocking them directly — coasting is often being lost. "
          "We don't silently do their work, and we loop in the organizer early.",
)

st.markdown("#### 5. Credit")
credit = st.text_input(
    "How is credit handled?",
    value="Each person presents the part they built. Contributions are recorded in "
          "Clearwork so the record is immutable.",
)

st.divider()
if st.button("Generate working agreement", type="primary"):
    lines = [f"# Working agreement — {team_name or 'our team'}", ""]
    lines.append("## Domain owners")
    for r, who in owners.items():
        lines.append(f"- **{r}:** {who or '_unassigned — assign before starting_'}")
    lines += [
        "",
        f"## How we decide\n{decision}",
        f"\n## Check-ins\n{checkins}",
        f"\n## If someone goes quiet\n{quiet}",
        f"\n## Credit\n{credit}",
        "",
        "_Agreed by all members at kickoff. Revisit at the midpoint check-in._",
    ]
    md = "\n".join(lines)
    st.success("Copy this, paste it in your team channel, and have everyone react ✅.")
    st.code(md, language="markdown")

    unassigned = [r for r, who in owners.items() if not who]
    if unassigned:
        st.warning("Still unassigned: " + ", ".join(unassigned)
                   + ". A team with no owner for a role is structurally weak.")
