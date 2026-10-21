# PIVOT V13 — Minimal, High-Contrast UI

PIVOT accepts student-prepared Word (`.docx`) and text-based PDF (`.pdf`) cases, uses Groq to create a four-round business simulation, evaluates decisions, and produces provisional rubric-based marks.

## Update existing Streamlit deployment
1. Replace `app.py` in your GitHub repository with this version.
2. Keep `requirements.txt` unless dependency changes are explicitly needed.
3. In Streamlit Community Cloud → App settings → Secrets, keep:

```toml
GROQ_API_KEY = "your-groq-api-key"
GROQ_MODEL = "openai/gpt-oss-20b"
```

Verify the model is available to your Groq account. Never put the API key in GitHub.

## UI changes
- High-contrast white input fields with dark text and readable placeholders.
- Clear form labels, helper text, and file upload area.
- Minimal neutral workspace with forest-green primary actions.
- Improved spacing, mobile layout, and card styling.

## Notes
Python syntax compilation passed. This does not substitute for a live Groq integration test. Use sample cases first; local SQLite may not persist reliably on cloud restarts. Automated marks should be reviewed before official use.


### V14 reliability fix

Simulation generation now repairs rounds where the LLM returns fewer or more than three valid choices. If a choice is missing, PIVOT adds a clearly labelled fallback option rather than stopping the entire submission. Review fallback options before using the simulation for formal teaching.
