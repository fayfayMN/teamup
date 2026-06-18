# 🤝 TeamUp

Form healthy teams for high-stakes competitions and projects — matched on
complementary skills, shared availability, and aligned commitment — then run a
guided kickoff that sets the team up to actually work well.

Companion to **Clearwork** (contribution tracking + verified resume cards).
See [plan.md](plan.md) for the full product vision.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`. A demo pool of 8 people is preloaded so you
can try matching immediately. All data persists to `teamup_state.json` and
survives restarts.

## How to use it

TeamUp walks a group of strangers from "we don't know each other" to "we have a
working agreement" in three steps. Use the sidebar to move between pages.

### 1. Join — everyone adds themselves to the pool
On the **Join** page, each person enters:
- **Strengths** — pick the skills you can actually deliver (these map to team
  roles: Build, Design, Pitch, Research, Organize)
- **Want to learn** — optional; enables mentor/learner matching
- **Availability** — the day-slots you can work (matching treats this as a near
  requirement — no shared time, no match)
- **Hours per week** and **commitment level** — *be honest here.* "Here to
  learn" vs. "here to win" mismatch is the single biggest silent team killer

Click **Add me to the pool**. Everyone who's joining does this once.

### 2. Match — generate balanced teams
On the **Match** page:
- Set the **target team size** (2–6)
- Click **Form teams**

For each proposed team you'll see:
- **Schedule cohesion** — how much the members' availability overlaps
- **Avg commitment** — the team's shared seriousness
- **Covered roles** — which of the four core roles are filled
- **Gap warnings** — e.g. "missing a presenter," mixed stakes, or weak schedule
  overlap, so you can fix it *before* you start, not after you lose

The output is the team **plus its gaps** — that's the whole point. When a team
looks right, click **Lock these teams**.

### 3. Team Kickoff — produce a working agreement
Each locked team runs the **Team Kickoff** page together (takes ~10 minutes):
- Assign **one owner per role** — not a single leader for everything
- Set the **decision rule**, **check-in times**, the **"if someone goes quiet"**
  rule, and how **credit** is handled
- Click **Generate working agreement**

You get a markdown agreement to paste into your team channel and have everyone
react ✅. This is your defense against free riders and credit-takers later.

## The product loop

```
TeamUp  →  Clearwork  →  verified resume card
form a     track who      proof of contribution
healthy    did what,      that flows back as a
team       fairly         trust signal next time
```

## Why it's free to run

Matching is a deterministic weighted score in pure Python — **no API key, no
LLM, no cost.** Every match comes with human-readable reasons, so it's
explainable by design and can't hallucinate.

## Tech

- **Streamlit** (multipage UI)
- **Pure-Python matching** (`teamup/match.py`) — no external services
- **JSON-file persistence** (`teamup_state.json`)

## Tests

```bash
python -m unittest discover tests
```

## License

MIT — see [LICENSE](LICENSE).
