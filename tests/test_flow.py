import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai_core.generator import (  # noqa: E402
    format_docx,
    format_html_preview,
    format_pdf,
    parse_terms,
    sanitize_text,
)

SAMPLE_TEXT = """1. PARTIES
This Agreement is entered into between Acme Corp and Jane Doe.

2. TERMS
Confidentiality period of 2 years; No disclosure to third parties.

3. GOVERNING LAW
This Agreement shall be governed by the laws of Delaware.
"""


def test_sanitize_text_strips_markdown_and_typography():
    dirty = "## Heading\n**bold** text with “quotes” and an — em dash"
    clean = sanitize_text(dirty)
    assert "#" not in clean
    assert "**" not in clean
    assert "“" not in clean and "”" not in clean
    assert "—" not in clean
    assert "-" in clean


def test_parse_terms_splits_and_cleans():
    terms = parse_terms("Term one; Term two.; Term three ")
    assert terms == ["Term one", "Term two", "Term three"]


def test_parse_terms_empty_string():
    assert parse_terms("") == []


def test_format_html_preview_contains_headings_and_paragraphs():
    html_out = format_html_preview(SAMPLE_TEXT)
    assert "<h3>1. PARTIES</h3>" in html_out
    assert "<p>" in html_out


def test_format_docx_returns_nonempty_bytes():
    docx_bytes = format_docx(SAMPLE_TEXT, "Non-Disclosure Agreement")
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0
    assert docx_bytes[:2] == b"PK"  # docx is a zip archive


def test_format_pdf_returns_nonempty_bytes():
    pdf_bytes = format_pdf(SAMPLE_TEXT, "Non-Disclosure Agreement")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes[:4] == b"%PDF"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    from legalEaseAPI.main import app

    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to LegalEase AI Legal Document Generator API"}


def test_generate_rejects_empty_fields(client):
    response = client.post(
        "/generate",
        json={"document_type": "NDA", "parties": "", "terms": "some terms", "dates": "2026"},
    )
    assert response.status_code == 400
    assert "parties" in response.json()["detail"]


def test_generate_success_with_mocked_gemini(client):
    with patch("legalEaseAPI.routes.GeminiDocumentGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate_document.return_value = SAMPLE_TEXT
        response = client.post(
            "/generate",
            json={
                "document_type": "Non-Disclosure Agreement",
                "parties": "Acme Corp and Jane Doe",
                "terms": "Confidentiality period of 2 years",
                "dates": "Effective Date: January 1, 2026",
            },
        )
    assert response.status_code == 200
    assert response.json()["document"] == SAMPLE_TEXT


def test_generate_returns_502_on_gemini_failure(client):
    from ai_core.gemini_generator import GeminiGenerationError

    with patch("legalEaseAPI.routes.GeminiDocumentGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate_document.side_effect = GeminiGenerationError(
            "boom"
        )
        response = client.post(
            "/generate",
            json={
                "document_type": "NDA",
                "parties": "A and B",
                "terms": "some terms",
                "dates": "2026",
            },
        )
    assert response.status_code == 502
