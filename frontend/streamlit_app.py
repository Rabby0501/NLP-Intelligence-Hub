# frontend/streamlit_app.py
import streamlit as st

import home
import sentiment
import semanticsearch
import summarizer
import imagecaption
import chromadb  # file is chromaDB.py

st.set_page_config(
    page_title="NLP Intelligence Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
try:
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

PAGES = {
    "🏠 Home": home,
    "💬 Sentiment Analyzer": sentiment,
    "🔍 Semantic Search": semanticsearch,
    "📝 Text Summarizer": summarizer,
    "🖼️ Image Captioning": imagecaption,
    "📦 ChromaDB Viewer": chromadb,
}

st.sidebar.title("NLP Intelligence Hub")
choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
page = PAGES[choice]
page.app()
