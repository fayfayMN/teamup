"""Team Kickoff — the differentiator. A guided 30-minute launch that outputs a
working agreement. This is where most matching tools stop and most teams fail."""

from datetime import date, timedelta

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

st.markdown("#### 2a. Scope & approval boundaries")
st.caption("Who decides alone vs. what needs the group — so no one person becomes the "
           "sole gatekeeper.")
boundaries = st.text_input(
    "Our boundary rule:",
    value="Owners decide within their area. Anything public-facing, team-branded, or "
          "cross-area needs a quick group sign-off — no single gatekeeper.",
)

st.markdown("#### 2b. Change & review window")
st.caption("Stops work being reversed or wiped on a whim.")
change_rule = st.text_input(
    "How do we change a decision already made?",
    value="A logged proposal gets a 48-hour written review window before it locks. "
          "Changing it needs a written counter-proposal, not a verbal override.",
)

st.markdown("#### 3. Check-ins")
checkins = st.text_input("When do we sync?",
                         value="At the midpoint and 2 hours before the deadline.")

st.markdown("#### 4. Communication style")
st.caption("Where decisions live and how fast people respond — the #1 thing teams "
           "never agree on until it's already a problem.")
comm_channel = st.text_input(
    "Where and how do we communicate?",
    value="One shared channel (Slack/Discord/group chat) for decisions — no side DMs "
          "for team business. Async by default; respond within 24 hours or flag "
          "you're blocked.",
)
escalation = st.text_input(
    "When something is stuck or urgent, what do we do?",
    value="Tag the domain owner directly. If no response in 24 hours, the integrator "
          "steps in. Anything time-sensitive gets a call, not a message.",
)

st.markdown("#### 5. If someone goes quiet")
quiet = st.text_input(
    "Our rule:",
    value="We ask what's blocking them directly — coasting is often being lost. "
          "We don't silently do their work, and we loop in the organizer early.",
)

st.markdown("#### 6. Credit")
credit = st.text_input(
    "How is credit handled?",
    value="Each person presents the part they built. Contributions are recorded in "
          "Clearwork so the record is immutable.",
)

st.markdown("#### 7. Review date")
st.caption("Put it on the calendar so the agreement stays current.")
review_by = st.date_input("Revisit this whole agreement by:",
                          value=date.today() + timedelta(days=90))

st.divider()
if st.button("Generate working agreement", type="primary"):
    lines = [f"# Working agreement — {team_name or 'our team'}", ""]
    lines.append("## Domain owners")
    for r, who in owners.items():
        lines.append(f"- **{r}:** {who or '_unassigned — assign before starting_'}")
    lines += [
        "",
        f"## How we decide\n{decision}",
        f"\n## Scope & approval boundaries\n{boundaries}",
        f"\n## Change & review window\n{change_rule}",
        f"\n## Check-ins\n{checkins}",
        f"\n## Communication style\n{comm_channel}",
        f"\n## Escalation\n{escalation}",
        f"\n## If someone goes quiet\n{quiet}",
        f"\n## Credit\n{credit}",
        "",
        "## Decision log (start here)",
        "Write one line every time you decide something — this is what stops silent "
        "reversals and lost credit.",
        "",
        "| Date | Decision | Owner | Approved by | Shared on |",
        "|------|----------|-------|-------------|-----------|",
        "| _(example)_ | the decision you made | (owner) | (who signed off) | (where you shared it) |",
        "|  |  |  |  |  |",
        "",
        f"## 📅 Review by\nRevisit this whole agreement by **{review_by}** so it "
        "stays current.",
        "",
        "_Agreed by all members at kickoff. Revisit at the midpoint check-in and on "
        "the review date above._",
    ]
    md = "\n".join(lines)
    st.success("Copy this, paste it in your team channel, and have everyone react ✅.")
    st.code(md, language="markdown")

    unassigned = [r for r, who in owners.items() if not who]
    if unassigned:
        st.warning("Still unassigned: " + ", ".join(unassigned)
                   + ". A team with no owner for a role is structurally weak.")
