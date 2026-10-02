import base64
import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai_core.generator import format_docx, format_html_preview, format_pdf  # noqa: E402
from config import API_BASE_URL, LOGO_PATH  # noqa: E402

st.set_page_config(
    page_title="LegalEase | AI Legal Document Generator",
    page_icon="⚖️",
    layout="centered",
)

CSS_PATH = Path(__file__).resolve().parent / "style.css"
st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)


def _logo_data_uri() -> str:
    if LOGO_PATH.exists():
        encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""


logo_uri = _logo_data_uri()
logo_img_tag = f'<img src="{logo_uri}" alt="LegalEase logo" />' if logo_uri else ""

st.markdown(
    f"""
    <div class="legalease-header">
        {logo_img_tag}
        <div class="title-block">
            <h1>LegalEase</h1>
            <p>AI-Powered Legal Document Generator</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""
if "document_type" not in st.session_state:
    st.session_state.document_type = ""

DOCUMENT_TYPES = [
    "Non-Disclosure Agreement",
    "Employment Contract",
    "Lease Agreement",
    "Service Agreement",
    "Partnership Agreement",
    "Other",
]

with st.form("document_form"):
    doc_type_choice = st.selectbox("Document Type", DOCUMENT_TYPES)
    custom_doc_type = ""
    if doc_type_choice == "Other":
        custom_doc_type = st.text_input("Specify document type")

    parties = st.text_input(
        "Parties",
        placeholder="e.g. Acme Corp (Disclosing Party) and Jane Doe (Receiving Party)",
    )
    terms = st.text_area(
        "Terms",
        placeholder="e.g. Confidentiality period of 2 years; No disclosure to third parties; "
        "Governing law is the State of Delaware",
        height=120,
    )
    dates = st.text_input("Dates", placeholder="e.g. Effective Date: January 1, 2026")

    submitted = st.form_submit_button("Generate Document")

if submitted:
    document_type = custom_doc_type.strip() if doc_type_choice == "Other" else doc_type_choice

    if not document_type or not parties.strip() or not terms.strip() or not dates.strip():
        st.error("Please fill in every field before generating a document.")
    else:
        with st.spinner("Drafting your document..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=90,
                )
                if response.status_code == 200:
                    st.session_state.generated_document = response.json()["document"]
                    st.session_state.document_type = document_type
                else:
                    detail = response.json().get("detail", response.text)
                    st.error(f"Could not generate document: {detail}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not reach the LegalEase API. Make sure the backend is running "
                    "(uvicorn legalEaseAPI.main:app --reload)."
                )
            except requests.exceptions.RequestException as exc:
                st.error(f"Request failed: {exc}")

if st.session_state.generated_document:
    st.markdown('<hr class="legalease-rule" />', unsafe_allow_html=True)
    st.markdown(
        f'<div class="legalease-sheet">{format_html_preview(st.session_state.generated_document)}'
        f'<div class="legalease-footer">LegalEase Inc. | contact@legalease.com | '
        f"All Rights Reserved.</div></div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        docx_bytes = format_docx(
            st.session_state.generated_document, st.session_state.document_type
        )
        st.download_button(
            "Download .docx",
            data=docx_bytes,
            file_name=f"{st.session_state.document_type or 'LegalEase'}.docx".replace(" ", "_"),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    with col2:
        pdf_bytes = format_pdf(
            st.session_state.generated_document, st.session_state.document_type
        )
        st.download_button(
            "Download .pdf",
            data=pdf_bytes,
            file_name=f"{st.session_state.document_type or 'LegalEase'}.pdf".replace(" ", "_"),
            mime="application/pdf",
        )
