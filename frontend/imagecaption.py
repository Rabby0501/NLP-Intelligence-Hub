# frontend/imagecaption.py
import streamlit as st
from utils_frontend import call_api


def app():
    st.markdown("## 🖼️ Image Captioning (Image ➜ Text)")
    st.write("Upload an image and the BLIP model will generate a natural-language caption.")

    file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if st.button("Generate Caption", type="primary"):
        if not file:
            st.warning("Please upload an image first.")
            return

        with st.spinner("Generating caption..."):
            files = {"file": (file.name, file.getvalue(), file.type)}
            data, err = call_api("/image-caption", method="post", files=files)

        if data and not err:
            st.subheader("Caption")
            st.write(data["caption"])

            st.image(file, use_column_width=True)

            with st.expander("Raw API Response"):
                st.json(data)
