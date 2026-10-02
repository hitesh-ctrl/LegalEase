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
docs/               Project phase deliverables & documentation (PDFs & Index)
frontend/           Streamlit app, pages, and styling
legalEaseAPI/       FastAPI app and routes
tests/              pytest suite
Image/Logo.png      Placeholder logo
```

## Documentation

All 27 project phase deliverables (PDFs) are organized in [`docs/`](docs/):

- 🎨 **Phase 1**: [`01_Ideation_and_Problem_Definition/`](docs/01_Ideation_and_Problem_Definition/) — Problem statements, brainstorming, empathy map
- 📐 **Phase 2**: [`02_Requirements_and_Architecture/`](docs/02_Requirements_and_Architecture/) — Tech stack, requirements, DFD, user stories, architecture
- 📅 **Phase 3**: [`03_Project_Planning_and_Agile/`](docs/03_Project_Planning_and_Agile/) — Milestones, sprint plan, progress tracking, agile management
- 🤖 **Phase 4**: [`04_AI_Data_and_Prompt_Engineering/`](docs/04_AI_Data_and_Prompt_Engineering/) — Data collection, model selection, prompt engineering
- 🧪 **Phase 5**: [`05_Development_and_Testing/`](docs/05_Development_and_Testing/) — Development integration, performance testing, UAT
- 🏆 **Phase 6**: [`06_Final_Deliverables_and_Assessment/`](docs/06_Final_Deliverables_and_Assessment/) — Final report, demo plan, features, grand assessment

For the full detailed index and direct links, see [`docs/README.md`](docs/README.md).

## Tests

```bash
pytest tests/ -v
```

## API

- `GET /` — health/welcome message
- `POST /generate` — body `{document_type, parties, terms, dates}` → `{document: "..."}`


Made with ❤️ by Hitesh, Navaneedan, Muthurajesh, Shrijesh, Saravanakumar

