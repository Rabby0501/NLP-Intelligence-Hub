# frontend/sentiment.py
import streamlit as st
from utils_frontend import call_api


def app():
    st.markdown("## 💬 Sentiment Analyzer")
    st.write(
        "Enter a sentence, review, or tweet. The system will clean the text, tokenize it, "
        "run it through a DistilBERT sentiment model, and display the prediction."
    )

    text = st.text_area(
        "Input text",
        placeholder="Example: I absolutely love this NLP project!",
        height=150,
    )

    if st.button("Analyze Sentiment", type="primary"):
        if not text.strip():
            st.warning("Please enter some text.")
            return

        with st.spinner("Analyzing sentiment..."):
            payload = {"text": text}
            data, err = call_api("/sentiment", json=payload)

        if data and not err:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Predicted Label", data["label"])
            with col2:
                st.metric("Confidence", f"{data['score']:.4f}")

            with st.expander("Raw API Response"):
                st.json(data)

    st.markdown("#### 📓 Pipeline Steps")
    st.write(
        """
        1. **Preprocessing** – lowercasing, URL/HTML removal, punctuation filtering  
        2. **Tokenization** – regex-based word splitting  
        3. **Model Inference** – DistilBERT sentiment classifier  
        4. **Logging** – input text stored in ChromaDB with metadata  
        """
    )
