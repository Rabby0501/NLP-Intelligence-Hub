# frontend/utils_frontend.py
import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("BACKEND_URL", os.getenv("API_BASE_URL", "http://localhost:8000"))


def call_api(path: str, method: str = "post", **kwargs):
    url = f"{API_BASE_URL}{path}"
    try:
        if method.lower() == "post":
            resp = requests.post(url, **kwargs, timeout=60)
        else:
            resp = requests.get(url, **kwargs, timeout=60)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return None, str(e)
