# PIVOT V11 — Groq Edition

PIVOT V11 uses Groq's OpenAI-compatible API for case analysis, simulation generation, decision feedback, and rubric-based grading. It uses the OpenAI Python SDK with Groq's documented base URL.

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to the root of your GitHub repository.
2. Deploy `app.py` at https://share.streamlit.io.
3. In Streamlit app Settings → Secrets, add:
   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   ```
4. Save and reboot the app. Never commit API keys or student data.

Get a Groq API key at https://console.groq.com/keys. Check current available models and rate limits at https://console.groq.com/docs/models and https://console.groq.com/docs/rate-limits. Free-tier availability and limits can change.

## Run locally
```bash
pip install -r requirements.txt
export GROQ_API_KEY="your-groq-api-key"
streamlit run app.py
```

## Student flow
1. Submit a student-prepared Word (`.docx`) or text-based PDF (`.pdf`) case.
2. Create a team name and passcode, enter course/section and case title, and enter the marks-report password.
3. Save the generated class code.
4. Teams join with the class code, team name, and passcode, then complete four decision rounds.
5. Groq provides decision feedback and generates a rubric-based result after all four rounds.

## Important limitations
- This build passed Python syntax and ZIP integrity checks, but has not been live-tested with a Groq API key.
- Automated marks should be treated as provisional and validated before consequential grading.
- Scanned PDFs need OCR; legacy `.doc` files need conversion to `.docx`.
- Local SQLite may not persist reliably across cloud restarts or concurrent sessions.
- Groq free-tier limits vary by model and account. Keep API keys in Streamlit Secrets, not GitHub.
