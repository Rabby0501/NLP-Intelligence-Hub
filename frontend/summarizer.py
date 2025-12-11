# frontend/summarizer.py
import streamlit as st
from utils_frontend import call_api


def app():
    st.markdown("## 📝 Text Summarizer")
    st.write("Paste a long paragraph or article and get a concise summary.")

    text = st.text_area(
        "Input article or paragraph",
        height=220,
        placeholder="Paste some long text here...",
    )

    if st.button("Summarize", type="primary"):
        if not text.strip():
            st.warning("Please enter some text.")
            return

        with st.spinner("Summarizing..."):
            payload = {"text": text}
            data, err = call_api("/summarize", json=payload)

        if data and not err:
            st.subheader("Summary")
            st.write(data["summary"])

            with st.expander("Raw API Response"):
                st.json(data)

    st.markdown("#### 📚 Notes")
    st.write(
        """
        - Input is cleaned and tokenized before feeding into the Transformer summarizer  
        - Summary output is also logged into ChromaDB (for analytics)  
        """
    )
