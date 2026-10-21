# PIVOT V10 — OpenAI Edition

PIVOT V10 uses the OpenAI API for case analysis, simulation generation, decision feedback, and rubric-based grading. The student-facing workflow and clearer V9 interface are retained.

## Run locally
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
# Optional: export OPENAI_MODEL="gpt-4.1-mini"
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to the root of your GitHub repository.
2. Deploy `app.py` at https://share.streamlit.io.
3. In app Settings → Secrets, add:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   OPENAI_MODEL = "gpt-4.1-mini"
   ```
4. Save and reboot the app. Never commit API keys or student data.

## Student flow
1. Submit a student-prepared Word (`.docx`) or text-based PDF (`.pdf`) case.
2. Create a team name and passcode, enter course/section and case title, and enter the marks-report password supplied by the course administrator.
3. Save the generated class code.
4. Teams join with the class code, team name, and passcode, then complete four decision rounds.
5. OpenAI provides decision feedback and generates a rubric-based result after all four rounds.

## Important limitations
- Automated marks should be treated as provisional and validated before consequential grading.
- Scanned PDFs need OCR; legacy `.doc` files need conversion to `.docx`.
- Local SQLite may not persist reliably across cloud restarts or concurrent sessions.
- API usage is billed separately from ChatGPT subscriptions. Keep API keys in Streamlit Secrets, not GitHub.
- The OpenAI API key is read from the `OPENAI_API_KEY` environment variable or Streamlit Secrets.
