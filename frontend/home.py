# frontend/home.py
import streamlit as st


def app():
    st.markdown('<div class="main-title"> NLP Intelligence Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">'
        "A unified dashboard for sentiment analysis, semantic search, QA, summarization, "
        "image captioning, and vector database exploration — all powered by deep learning."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ML / NLP Modules", "4", "Transformer-based")
    with col2:
        st.metric("Vector DB Backend", "ChromaDB", "Semantic Search")
    with col3:
        st.metric("Deployment", "3 Containers", "Docker Compose")

    st.markdown("### 🔧 System Overview")
    st.write(
        """
        **Backend (FastAPI)**  
        - Sentiment analysis (DistilBERT)  
        - Semantic search Sentence-BERT + ChromaDB  
        - Text summarization (Seq2Seq Transformer)  
        - Image captioning (BLIP multimodal model)  

        **Frontend (Streamlit UI)**  
        - Modern dark-themed dashboard  
        - Individual tools on separate pages  
        - Live results with confidence scores & retrieved contexts  

        **Vector Database (ChromaDB)**  
        - Stores text embeddings + metadata  
        - Used for semantic search, QA and logging all user interactions  
        """
    )

    st.markdown("### 📦 Project Highlights")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            - ✅ Deep learning transformer models  
            - ✅ Custom text preprocessing & tokenization  
            - ✅ Semantic search pipeline with embeddings  
            - ✅ Vector DB integration (ChromaDB)  
            """
        )
    with c2:
        st.markdown(
            """
            - ✅ Streamlit UI + FastAPI backend  
            - ✅ Multi-container Docker Compose  
            - ✅ Logging into ChromaDB for auditing  
            - ✅ Ready for GitHub + report screenshots  
            """
        )
