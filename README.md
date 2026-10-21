# PIVOT — Phase 3: Company Wars

Phase 3 builds on the Phase 1 reliability work and Phase 2 Business Arena, adding a classroom competition layer.

## What's new

- **Company Wars leaderboard:** teams using the same class code can compare progress and a company-health index.
- **Shared market pulses:** every team sees the same round-specific external pressure (demand signal, supply shock, competitive response, board review).
- **Company health index:** equal-weight average of cash, service, trust, morale, and risk resilience (100 minus risk), with each metric bounded to 0–100.
- **Progress-aware standings:** completed rounds are prioritized first; health score breaks ties. This discourages an unplayed team from ranking first simply because it remains at baseline.
- **Live in-play standings:** teams see their current rank, health score, and round progress in the simulation workspace.
- **Testable competitive engine:** shared pulses, metric clamping, score calculation, and rank ordering are isolated in `arena_engine.py`.

The shared market pulse is common context and does not itself modify the deterministic business metrics. Teams' chosen options and bounded rationale adjustments determine those metrics. Real-time multiplayer synchronization and simultaneous market-clearing economics are not implemented in this phase.

## Deploy to Streamlit Community Cloud

1. Download and extract this ZIP.
2. In the `ksmakkar/pivot-v8` GitHub repository, replace `app.py` with `pivot_phase1/app.py`.
3. Add the new `arena_engine.py` file to the repository root (same directory as `app.py`).
4. Keep `requirements.txt` aligned with the included file, then commit the changes.
5. Streamlit Community Cloud should redeploy automatically.
6. Test with a non-confidential case and at least two team names using the same class code.

Keep `GROQ_API_KEY` in Streamlit **Settings → Secrets**, not in GitHub. The app uses `GROQ_MODEL` if configured and otherwise defaults to `openai/gpt-oss-20b`.

Example Secrets:

```toml
GROQ_API_KEY = "your-existing-groq-api-key"
GROQ_MODEL = "openai/gpt-oss-20b"
```

Use a model currently available to your Groq account; model availability can change.

## Verification

Run locally from this folder:

```bash
python -m py_compile app.py arena_engine.py
pytest -q
```

The included tests cover the existing simulation schema repair plus Phase 3 market-pulse boundaries, metric clamping, risk inversion, and rank ordering. These checks do not verify live Groq calls or the deployed Streamlit app.

## Important limitations

- The leaderboard is visible to anyone who knows the class code; use non-sensitive team names.
- The company-health index is a game score, not an academic grade or validated measure of business performance.
- SQLite persistence on Streamlit Community Cloud may not survive restarts/rebuilds. Use a persistent mounted volume or managed database for durable classroom records.
- The market pulses are round-specific shared prompts, not live news feeds or simulated market-clearing events.
- Automated grading remains provisional and should be reviewed before high-stakes use.
