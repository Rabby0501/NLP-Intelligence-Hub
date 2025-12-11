#  A Multi-Model NLP System with Transformers, Embeddings, Vector Search, Image Captioning & Full Dockerized Deployment

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-blue" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/ChromaDB-black" alt="ChromaDB">
  <img src="https://img.shields.io/badge/Docker-2496ED" alt="Docker">
  <img src="https://img.shields.io/badge/Python-3.9%2B-yellowgreen" alt="Python">
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-orange" alt="HuggingFace">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## 1. Project Overview
NLP Intelligence Hub is a production-style, multi-model Natural Language Processing system built using:

- **Deep Learning Models**:
  - Sentiment Analysis (Transformer, offline)
  - Semantic Search (Sentence-BERT embeddings + ChromaDB)
  - Summarization (distilbart-cnn-12-6 Transformer)
  - Image Captioning (BLIP Vision-Language Mode

- **Vector Database**:
  - ChromaDB for storing embeddings, logs, user queries, metadata

- **Full Preprocessing Pipeline**:
  - Text Cleaning
  - Tokenization
  - Normalization
  - Metadata creation (e.g., timestamps, doc_type, source, id)
 
- **Modern Frontend**:
  - Streamlit UI with multiple NLP tools
  - Visual results + dark theme
  - Navigation system
 
- **Containerized Deployment**:
  - 3 Docker Services:
    - backend (FastAPI)
    - frontend (Streamlit)
    - chromadb (vector store)

