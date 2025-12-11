# frontend/chromaDB.py
import pandas as pd
import streamlit as st
from utils_frontend import call_api


def app():
    st.markdown("## 📦 ChromaDB Viewer")
    st.write(
        "Inspect what is stored in your vector database: logged user inputs, summaries, "
        "System seed documents."
    )

    if st.button("Refresh ChromaDB Snapshot", type="primary"):
        with st.spinner("Fetching data from backend..."):
            data, err = call_api("/chroma-info", method="get")

        if data and not err:
            st.markdown(f"**Collection**: `{data['collection_name']}`")
            st.markdown(f"**Document count**: `{data['document_count']}`")

            docs = data.get("documents", [])
            if docs:
                # Flatten metadata for a nicer table
                rows = []
                for d in docs:
                    meta = d.get("metadata") or {}
                    rows.append(
                        {
                            "id": d.get("id"),
                            "text": d.get("text"),
                            "doc_type": meta.get("doc_type"),
                            "source": meta.get("source"),
                            "created_at_utc": meta.get("created_at_utc"),
                        }
                    )
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No documents found in ChromaDB yet.")

            with st.expander("Raw API Response"):
                st.json(data)
    else:
        st.info("Click **Refresh ChromaDB Snapshot** to load current data.")
