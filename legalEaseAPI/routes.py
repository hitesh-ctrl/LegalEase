from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator, GeminiGenerationError

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):
    fields = {
        "document_type": request.document_type,
        "parties": request.parties,
        "terms": request.terms,
        "dates": request.dates,
    }
    empty_fields = [name for name, value in fields.items() if not value.strip()]
    if empty_fields:
        raise HTTPException(
            status_code=400,
            detail=f"The following fields cannot be empty: {', '.join(empty_fields)}.",
        )

    try:
        generator = GeminiDocumentGenerator()
        document_text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"document": document_text}
