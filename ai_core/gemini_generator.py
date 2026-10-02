import time

import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL

_EXTRA_GUIDANCE = {
    "nda": (
        "This is a Non-Disclosure Agreement. Clearly define 'Confidential Information', "
        "specify the obligations of the receiving party, the duration of confidentiality "
        "(survival period), and permitted exceptions (e.g. information already public, "
        "independently developed, or required by law)."
    ),
    "non-disclosure agreement": (
        "This is a Non-Disclosure Agreement. Clearly define 'Confidential Information', "
        "specify the obligations of the receiving party, the duration of confidentiality "
        "(survival period), and permitted exceptions (e.g. information already public, "
        "independently developed, or required by law)."
    ),
    "employment contract": (
        "This is an Employment Contract. Include job title and duties, compensation and "
        "benefits, work schedule, probation period, termination conditions and notice "
        "period, and confidentiality/non-compete expectations where appropriate."
    ),
    "employment agreement": (
        "This is an Employment Contract. Include job title and duties, compensation and "
        "benefits, work schedule, probation period, termination conditions and notice "
        "period, and confidentiality/non-compete expectations where appropriate."
    ),
    "lease agreement": (
        "This is a Lease Agreement. Include the property description, lease term, rent "
        "amount and due date, security deposit terms, maintenance responsibilities, and "
        "conditions for renewal or termination."
    ),
    "lease": (
        "This is a Lease Agreement. Include the property description, lease term, rent "
        "amount and due date, security deposit terms, maintenance responsibilities, and "
        "conditions for renewal or termination."
    ),
}


class GeminiGenerationError(Exception):
    pass


class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        if not self.api_key:
            raise GeminiGenerationError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def _build_prompt(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        doc_type_lower = document_type.strip().lower()
        extra_guidance = ""
        for key, guidance in _EXTRA_GUIDANCE.items():
            if key in doc_type_lower:
                extra_guidance = guidance
                break

        prompt = f"""You are a professional legal drafting assistant. Draft a formal, complete
legal document of the following type: {document_type}.

Use the information below to populate the document:
- Parties: {parties}
- Terms: {terms}
- Dates: {dates}

Formatting requirements:
- Produce plain text only (no markdown symbols such as ** or ##).
- Use numbered sections (1., 2., 3., ...) with clear, bold-style ALL-CAPS section headings
  on their own line (e.g. "1. PARTIES").
- Include, at minimum, the following sections in a sensible order: Parties, Effective Date,
  the user's provided Terms (expand and clarify them into clean legal clauses), Governing
  Law, Severability, Entire Agreement, and a Signature block for each party with name,
  signature line, and date.
- Write in formal legal language appropriate for the document type.
{extra_guidance}

Return only the final document text, ready to be inserted into a formal contract template.
"""
        return prompt

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = self._build_prompt(document_type, parties, terms, dates)

        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = self.model.generate_content(prompt)
                text = (getattr(response, "text", "") or "").strip()
                if not text:
                    raise GeminiGenerationError("Gemini returned an empty response.")
                return text
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < 2:
                    time.sleep(2 ** attempt)

        raise GeminiGenerationError(f"Gemini generation failed after retries: {last_error}")
