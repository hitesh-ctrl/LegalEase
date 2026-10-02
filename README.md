# LegalEase

AI-powered legal document generator. FastAPI backend + Streamlit frontend, drafting
documents with the Google Gemini API.

## Stack

- Python 3.10+
- FastAPI (backend API)
- Streamlit (frontend)
- Google Gemini API (`google-generativeai`)
- python-docx / fpdf2 for export formats

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set GEMINI_API_KEY
```

## Run

```bash
./run.sh
```

This starts the FastAPI backend on `http://127.0.0.1:8000` and the Streamlit frontend on
`http://localhost:8501`.

To run them separately:

```bash
uvicorn legalEaseAPI.main:app --reload
streamlit run frontend/app.py
```

## Project layout

```
ai_core/            Gemini integration + document formatters (docx/pdf/html)
frontend/            Streamlit app, pages, and styling
legalEaseAPI/       FastAPI app and routes
tests/              pytest suite
Image/Logo.png      Placeholder logo
```

## Tests

```bash
pytest tests/ -v
```

## API

- `GET /` — health/welcome message
- `POST /generate` — body `{document_type, parties, terms, dates}` → `{document: "..."}`
