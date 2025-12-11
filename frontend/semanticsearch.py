# frontend/semanticsearch.py
import streamlit as st
from utils_frontend import call_api


def app():
    st.markdown("## 🔍 Semantic Search")
    st.write(
        "Type a query. We preprocess it, convert it to an embedding using Sentence-BERT, "
        "and search over the ChromaDB collection."
    )

    query = st.text_input(
        "Search query",
        placeholder="Example: What can deep learning be used for?",
    )
    top_k = st.slider("Number of results", 1, 10, 5)

    if st.button("Search", type="primary"):
        if not query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("Searching semantic space..."):
            payload = {"query": query, "top_k": top_k}
            data, err = call_api("/semantic-search", json=payload)

        if data and not err:
            for r in data["results"]:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="badge">ID: {r['id']}</div>
                        <div style="margin-top:0.4rem;">{r['text']}</div>
                        <div style="margin-top:0.3rem; font-size:0.8rem; color:#9ca3af;">
                            Distance score: {r['score']:.4f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.expander("Raw API Response"):
                st.json(data)

    st.markdown("#### 🧠 How it works")
    st.write(
        """
        - Query is **cleaned + tokenized**  
        - Sentence-BERT encoder generates a dense vector  
        - Vector is compared to stored document embeddings in **ChromaDB**  
        - Top-𝑘 similar texts are returned  
        """
    )
