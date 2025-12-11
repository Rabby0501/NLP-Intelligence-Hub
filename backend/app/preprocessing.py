# backend/app/preprocessing.py
import re
from typing import List, Dict, Any
from datetime import datetime


def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - convert to lowercase
    - remove URLs and HTML
    - keep only letters/numbers/basic punctuation
    - collapse extra whitespace
    """
    if not isinstance(text, str):
        text = str(text)

    text = text.lower()
    # remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    # remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # keep only letters, numbers, spaces, and basic punctuation
    text = re.sub(r"[^a-z0-9\s.,!?']", " ", text)
    # collapse spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """
    Very simple tokenization using regex.
    (You can mention this as the tokenization step in your report.)
    """
    text = clean_text(text)
    return re.findall(r"\b\w+\b", text)


def preprocess_for_model(text: str) -> str:
    """
    High-level preprocessing for model input.
    (Right now cleaning is enough; later you could join tokens back if needed.)
    """
    return clean_text(text)


def build_metadata(source: str, doc_type: str) -> Dict[str, Any]:
    """
    Metadata that we store together with each document in ChromaDB.
    """
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "source": source,
        "doc_type": doc_type,
        "created_at_utc": now,
    }
