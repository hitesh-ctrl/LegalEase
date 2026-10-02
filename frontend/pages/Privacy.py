from pathlib import Path

import streamlit as st

st.set_page_config(page_title="LegalEase | Privacy Policy", page_icon="⚖️", layout="centered")

CSS_PATH = Path(__file__).resolve().parent.parent / "style.css"
st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="legalease-header">
        <div class="title-block">
            <h1>Privacy Policy</h1>
            <p>LegalEase</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="legalease-sheet">
    <h3>1. INFORMATION YOU PROVIDE</h3>
    <p>LegalEase processes the document details you enter (parties, terms, and dates) solely
    to generate your requested legal document. This information is sent to the Google Gemini
    API for generation and is not stored permanently by LegalEase beyond your active session.</p>

    <h3>2. NO SALE OF DATA</h3>
    <p>LegalEase does not sell, rent, or share your information with third parties for
    marketing purposes.</p>

    <h3>3. THIRD-PARTY SERVICES</h3>
    <p>Document generation is powered by Google's Gemini API, which is subject to Google's
    own privacy practices and terms.</p>

    <h3>4. CONTACT</h3>
    <p>Questions about this policy may be directed to contact@legalease.com.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
