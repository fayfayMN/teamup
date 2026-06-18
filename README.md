# 🤝 TeamUp

Form healthy teams for high-stakes competitions and projects — matched on
complementary skills, shared availability, and aligned commitment — then run a
guided kickoff that sets the team up to actually work well.

Companion to **Clearwork** (contribution tracking + verified resume cards).
See [plan.md](plan.md) for the full product vision.

---

## Quick start (local, no setup)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`. The app starts empty — real people join on
the **Join** page. Click **Load demo data** to add 8 sample people and try
matching right away. Click **Clear pool** to reset.

Data is saved to `teamup_state.json` locally and survives restarts.

---

## Deploying to Streamlit Community Cloud (owner setup — done once)

> **Members never touch this.** You deploy the app once, Streamlit gives you a
> public URL, and members just open that link in any browser to sign up.

Streamlit Cloud's filesystem is **ephemeral** — files get wiped whenever the
app sleeps or redeploys. Wire up Google Sheets first so signup data survives.

### Step 1 — Create the Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new blank spreadsheet.
2. Name it **TeamUp** (or anything you like).
3. Create two worksheets (tabs at the bottom):
   - Rename **Sheet1** → `Pool`
   - Add a second sheet, name it `Teams`
4. In the **Pool** tab, add these exact headers in row 1:

   ```
   id | name | skills | wants_to_learn | availability | hours_per_week | commitment
   ```

   (one header per column, A through G)

5. In the **Teams** tab, add these headers in row 1:

   ```
   team_number | members_json
   ```

6. Copy the spreadsheet URL from your browser — you'll need it shortly.

### Step 2 — Create a Google Cloud service account

> This lets TeamUp read and write your sheet securely without using your
> personal Google login.

1. Go to [console.cloud.google.com](https://console.cloud.google.com).
2. Create a new project (or pick an existing one). Name it anything, e.g. `teamup`.
3. In the search bar, search for **Google Sheets API** and click **Enable**.
4. Also enable the **Google Drive API** the same way.
5. Go to **IAM & Admin → Service Accounts → Create Service Account**.
   - Name: `teamup` (any name)
   - Click **Create and Continue**, skip the optional role steps, click **Done**.
6. Click on the service account you just created → **Keys** tab → **Add Key →
   Create new key → JSON**. A `.json` file downloads — keep it safe.
7. Open that JSON file in a text editor. You'll copy values from it in Step 4.

### Step 3 — Share the spreadsheet with the service account

1. Open the downloaded JSON file and copy the `client_email` value.
   It looks like: `teamup@your-project.iam.gserviceaccount.com`
2. Open your Google Sheet, click **Share** (top right).
3. Paste that email address and give it **Editor** access. Click **Send**.

The service account can now read and write your sheet.

### Step 4 — Set up secrets

**For local development:**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and fill in:

```toml
[connections.gsheets]
spreadsheet    = "https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit"
type           = "service_account"
private_key_id = "..."   # from the JSON key file
private_key    = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email   = "teamup@your-project.iam.gserviceaccount.com"
client_id      = "..."
token_uri      = "https://oauth2.googleapis.com/token"
```

Copy each value directly from your downloaded JSON key file.
**Never commit `secrets.toml`** — it's already gitignored.

**For Streamlit Community Cloud:**

1. In your Streamlit Cloud dashboard, open your app → **Settings → Secrets**.
2. Paste the same content you put in `secrets.toml` directly into the text box.
3. Click **Save**. The app will restart and pick up the credentials.

### Step 5 — Deploy (owner only, done once)

1. Push this repo to GitHub (if you haven't already).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch `main`, main file `app.py`.
4. Click **Deploy**.

Streamlit gives you a public URL like `https://teamup-mac.streamlit.app`.
**Share that link with your members — they don't install anything, they just
open it in a browser and fill in the Join form.** Every submission writes a row
into your Google Sheet permanently, surviving any sleep, restart, or redeploy.

---

## How to use the app

TeamUp walks a group of strangers from "we don't know each other" to "we have a
working agreement" in three steps.

### 1. Join — everyone adds themselves

Each person goes to the **Join** page and enters:

- **Strengths** — the skills you can actually deliver. These map to team roles:
  Build, Design, Pitch, Research, Organize.
- **Want to learn** — optional. Enables mentor/learner pairing.
- **Availability** — the day-slots you can work. Zero shared time = no match.
- **Hours per week** and **commitment level** — be honest. "Here to learn" vs.
  "here to win" mismatch is the #1 silent team killer.

Click **Add me to the pool**. Every participant does this once.

### 2. Match — generate balanced teams

On the **Match** page:

- Set the **target team size** (2–6).
- Click **Form teams**.

For each proposed team you'll see:

- **Schedule cohesion** — how much members' availability overlaps.
- **Avg commitment** — the team's shared seriousness level.
- **Covered roles** — which of the four core roles are filled.
- **Gap warnings** — missing a presenter, mixed stakes, or weak schedule
  overlap flagged *before you start*, not after you lose.

When the teams look right, click **Lock these teams**.

### 3. Team Kickoff — generate a working agreement

Each locked team runs the **Team Kickoff** page together (~10 minutes):

- Assign **one owner per role** — not a single leader for everything.
- Set the decision rule, check-in times, the "if someone goes quiet" rule, and
  how credit is handled at the end.
- Click **Generate working agreement**.

You get markdown to paste into your team channel. Have everyone react ✅.
This is your defense against free riders and credit-takers later.

---

## The product loop

```
TeamUp  →  Clearwork  →  verified resume card
form a     track who      proof of contribution
healthy    did what,      flows back as a trust
team       fairly         signal for next match
```

---

## Why it's free to run

Matching is a deterministic weighted score in pure Python — **no API key, no
LLM, no cost.** Every match comes with human-readable reasons, so it's
explainable and can't hallucinate.

Google Sheets is also **free** — the standard Google account tier is more than
enough for a competition signup pool.

---

## Tech stack

| Layer | Choice |
|-------|--------|
| App / UI | Streamlit (multipage) |
| Matching | Pure Python (`teamup/match.py`) |
| Persistence — local | JSON file (`teamup_state.json`) |
| Persistence — deployed | Google Sheets (`st-gsheets-connection`) |
| Auth | None for v1 — URL-based access |

---

## Tests

```bash
python -m unittest discover tests
```

---

## License

MIT — see [LICENSE](LICENSE).
