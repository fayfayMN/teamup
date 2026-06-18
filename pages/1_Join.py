"""Join — intake. Good matches depend entirely on what we collect here."""

import streamlit as st

from teamup.store import init_state, save
from teamup.match import Profile, SKILLS, COMMITMENT

st.set_page_config(page_title="Join · TeamUp", page_icon="✍️", layout="wide")
init_state(st)

st.title("✍️ Join the pool")
st.caption("Be honest about availability and commitment — mismatched stakes is the "
           "single biggest silent team killer.")

SLOTS = ["mon-eve", "tue-eve", "wed-eve", "thu-eve", "fri-eve", "sat-day", "sun-day"]

with st.form("join"):
    name = st.text_input("Name")
    skills = st.multiselect("What you're good at (pick your real strengths)", SKILLS)
    learn = st.multiselect("What you want to learn (optional)", SKILLS)
    avail = st.multiselect("When you're available", SLOTS, default=["sat-day"])
    hours = st.slider("Hours per week you can commit", 1, 40, 8)
    commit = st.select_slider(
        "How serious are you?",
        options=list(COMMITMENT.keys()),
        format_func=lambda k: COMMITMENT[k],
        value=2,
    )
    submitted = st.form_submit_button("Add me to the pool")

if submitted:
    if not name or not skills:
        st.error("Name and at least one skill are required.")
    else:
        pid = f"p{len(st.session_state.pool) + 1}_{name.lower().replace(' ', '')}"
        st.session_state.pool.append(Profile(
            id=pid, name=name, skills=skills, wants_to_learn=learn,
            availability=avail, hours_per_week=hours, commitment=commit,
        ))
        save(st)
        st.success(f"Added {name}. Head to **Match** to form teams.")

st.divider()
st.markdown("#### Current pool")
if not st.session_state.pool:
    st.caption("Empty.")
else:
    st.dataframe(
        [{
            "Name": p.name,
            "Roles": ", ".join(sorted(p.roles())) or "—",
            "Available": ", ".join(p.availability),
            "Hrs/wk": p.hours_per_week,
            "Commitment": COMMITMENT[p.commitment],
        } for p in st.session_state.pool],
        use_container_width=True, hide_index=True,
    )
