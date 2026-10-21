# PIVOT V8 — Autonomous Gemini Strategy Lab

PIVOT V8 removes instructor controls. Students upload their team's case as Word (.docx) or text-based PDF (.pdf). Gemini extracts the case logic, generates four decision rounds and three options per round, evaluates team rationales, simulates business consequences, and awards rubric-based provisional marks after round four. The instructor role is read-only marks/report access.

## Run locally
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
streamlit run app.py
```

## Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to the root of a GitHub repository.
2. Deploy `app.py` on https://share.streamlit.io.
3. In app Settings → Secrets, add:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
```
4. Reboot the app. Do not commit API keys or database files.

## Flow
1. A student representative uploads the case and starts the simulation.
2. PIVOT extracts the text and Gemini generates four case-grounded rounds.
3. The uploader receives a classroom code. Other teams join with that code.
4. Each team completes four rounds independently; each decision is evaluated with case-grounded AI feedback and business-metric effects.
5. After the fourth round, Gemini scores the team using the rubric (30% decision quality, 25% case evidence, 20% strategic coherence, 15% outcome management, 10% reflection). The read-only results page provides marks and CSV export.

## Important limitations
- This is a prototype, not a validated grading system. Marks are provisional; provide human review/appeal for consequential grading.
- Gemini outputs may be inaccurate or inconsistent. The app validates JSON shape but cannot guarantee pedagogical validity.
- Scanned PDFs require OCR. Legacy `.doc` files must be converted to `.docx`.
- Local SQLite is not suitable for reliable persistence across cloud restarts or concurrent classes. For real deployment, use managed PostgreSQL, access controls, backups, rate limits, and privacy review.
- The API key is stored only in deployment secrets/environment; never put it in the repository.
