from pathlib import Path

import streamlit as st

st.set_page_config(page_title="LegalEase | Terms of Use", page_icon="⚖️", layout="centered")

CSS_PATH = Path(__file__).resolve().parent.parent / "style.css"
st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="legalease-header">
        <div class="title-block">
            <h1>Terms of Use</h1>
            <p>LegalEase</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="legalease-sheet">
    <h3>1. NO LEGAL ADVICE</h3>
    <p>LegalEase generates draft documents using an AI language model. These drafts are
    provided for informational purposes only and do not constitute legal advice. You should
    have any generated document reviewed by a licensed attorney before relying on it.</p>

    <h3>2. NO ATTORNEY-CLIENT RELATIONSHIP</h3>
    <p>Use of this application does not create an attorney-client relationship between you
    and LegalEase Inc. or any of its contributors.</p>

    <h3>3. ACCURACY</h3>
    <p>While LegalEase strives to produce coherent and well-structured documents, AI-generated
    text may contain errors, omissions, or clauses unsuitable for your jurisdiction. You are
    responsible for verifying the accuracy and suitability of any generated content.</p>

    <h3>4. ACCEPTANCE</h3>
    <p>By using LegalEase, you acknowledge and accept the terms described above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
