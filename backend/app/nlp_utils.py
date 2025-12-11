# backend/app/nlp_utils.py
import io
import os
from typing import List, Tuple
from uuid import uuid4

import chromadb
from chromadb.config import Settings
from PIL import Image

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoProcessor,
)
from sentence_transformers import SentenceTransformer
from transformers import BlipForConditionalGeneration

from .preprocessing import preprocess_for_model, clean_text, build_metadata

# ----------------- MODEL PATHS -----------------

BASE_MODEL_DIR = os.getenv(
    "MODEL_DIR",
    os.path.join(os.path.dirname(__file__), "..", "models")
)

SENTIMENT_MODEL_DIR = os.path.join(BASE_MODEL_DIR, "sentiment")
EMBED_MODEL_DIR = os.path.join(BASE_MODEL_DIR, "embedder")
SUMMARY_MODEL_DIR = os.path.join(BASE_MODEL_DIR, "summarizer")
BLIP_MODEL_DIR = os.path.join(BASE_MODEL_DIR, "blip")

# ----------------- SENTIMENT -----------------

_sent_tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_DIR)
_sent_model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_DIR)

_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=_sent_model,
    tokenizer=_sent_tokenizer,
)


def analyze_sentiment(text: str) -> Tuple[str, float]:
    processed = preprocess_for_model(text)
    res = _sentiment_pipeline(processed)[0]
    return res["label"], float(res["score"])


# ----------------- EMBEDDINGS + CHROMA -----------------

_embedder = SentenceTransformer(EMBED_MODEL_DIR)


def get_embedding(text: str) -> List[float]:
    processed = preprocess_for_model(text)
    emb = _embedder.encode(processed, convert_to_numpy=True).tolist()
    return emb


def get_chroma_client():
    host = os.getenv("CHROMA_HOST", "localhost")
    port = int(os.getenv("CHROMA_PORT", "8000"))
    client = chromadb.HttpClient(
        host=host,
        port=port,
        settings=Settings(allow_reset=False),
    )
    return client


def get_or_create_collection():
    client = get_chroma_client()
    col = client.get_or_create_collection("nlp_corpus")
    return col


def add_document(text: str, doc_type: str, source: str = "app") -> str:
    """
    Add a document + embedding + metadata into ChromaDB.
    Used for logging user interactions (queries, answers, summaries, etc.).
    """
    col = get_or_create_collection()

    cleaned = clean_text(text)
    embedding = get_embedding(cleaned)
    doc_id = f"{doc_type}-{uuid4().hex}"
    metadata = build_metadata(source=source, doc_type=doc_type)

    col.add(
        documents=[cleaned],
        embeddings=[embedding],
        ids=[doc_id],
        metadatas=[metadata],
    )
    return doc_id


def ensure_sample_data_loaded():
    """
    Seed the database with a few default docs if it's empty.
    """
    col = get_or_create_collection()

    if col.count() > 0:
        return

    docs = [
        "Streamlit is a great framework for building data apps.",
        "Transformers have changed the NLP landscape.",
        "Deep learning enables powerful applications such as image captioning.",
        "Sentiment analysis helps companies understand customer feedback.",
        "Question answering systems can respond to user queries using context.",
    ]
    docs = [clean_text(t) for t in docs]
    ids = [f"doc-{i}" for i in range(len(docs))]
    embeddings = [get_embedding(t) for t in docs]

    col.add(documents=docs, embeddings=embeddings, ids=ids)


def semantic_search(query: str, top_k: int = 5):
    ensure_sample_data_loaded()
    col = get_or_create_collection()

    q_emb = get_embedding(query)
    res = col.query(
        query_embeddings=[q_emb],
        n_results=top_k,
    )
    results = []
    for idx in range(len(res["ids"][0])):
        results.append(
            {
                "id": res["ids"][0][idx],
                "text": res["documents"][0][idx],
                "score": float(res["distances"][0][idx]),
                "metadata": res["metadatas"][0][idx],
            }
        )
    return results


# ----------------- SUMMARIZATION -----------------

_sum_tokenizer = AutoTokenizer.from_pretrained(SUMMARY_MODEL_DIR)
_sum_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY_MODEL_DIR)
_summarizer_pipeline = pipeline(
    "summarization",
    model=_sum_model,
    tokenizer=_sum_tokenizer,
)


def summarize_text(text: str, max_len: int = 120) -> str:
    processed = preprocess_for_model(text)
    res = _summarizer_pipeline(
        processed,
        max_length=max_len,
        min_length=30,
        do_sample=False,
    )
    return res[0]["summary_text"]


# ----------------- IMAGE CAPTIONING (BLIP) -----------------

_blip_processor = AutoProcessor.from_pretrained(BLIP_MODEL_DIR)
_blip_model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_DIR)


def caption_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = _blip_processor(images=image, return_tensors="pt")
    out = _blip_model.generate(**inputs, max_new_tokens=30)
    caption = _blip_processor.decode(out[0], skip_special_tokens=True)
    return caption
