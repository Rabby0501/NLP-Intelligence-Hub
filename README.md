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

---

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

---

## 2. System Architecture
The application is composed of **three independent Docker services**:

| Service      | Port | Responsibility                |
| ------------ | ---- | ----------------------------- |
| **frontend** | 8501 | Streamlit web UI              |
| **backend**  | 8000 | FastAPI NLP inference & logic |
| **chromadb** | 8001 | Vector database (ChromaDB)    |


### Key Design Guarantees
- Backend never renders UI
- Frontend never loads ML models
- Vector database runs in a separate container
- Models are loaded locally (offline, no internet dependency)
- All communication happens via REST APIs

---

## 3. Project Structure

```
NLP-Intelligence-Hub/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── nlp_utils.py         # NLP pipelines & logic
│   │   ├── preprocessing.py     # Text preprocessing
│   │   ├── models.py            # Pydantic schemas
│   │
│   ├── models/
│   │   ├── sentiment/           # Sentiment transformer model
│   │   ├── embedder/            # Sentence-BERT embedder
│   │   ├── summarizer/          # Text summarization model
│   │   └── blip/                # Image captioning model
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py         # Streamlit UI This is the main file. We also have individual file-based models, and they connect with the API
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```
---

## 4. 🧠 Embedding & Vector Search
- Sentence-BERT generates dense vector embeddings
- Vectors are stored in ChromaDB
- Each document is saved with:
  - ID
  - Text
  - Metadata (type, timestamp)
- Semantic search retrieves Top-K nearest neighbors

---

## 5. 🐳 Docker & Deployment
### Dockerfile Design
- Lightweight base images (python:3.x-slim)
- Layered dependency installation
- Explicit port exposure
- Environment-based configuration

### Docker Compose
- Multi-container orchestration
- Isolated services
- Internal networking
- Reproducible deployment

---

## 6. Prerequisites

Ensure the following are installed:

- Docker (v20+)
- Docker Compose v2
- Python 3.10
- Git

Verify for Linux:
```
docker --version
docker compose version
Python3 --version
git --version
```

---

## 7. How to Run the Project
### 1. Clone Repository
```
git clone https://github.com/Rabby0501/NLP-Intelligence-Hub.git
cd NLP-Intelligence-Hub
```

### 2. Build Containers
```
docker compose build
```

### 3. Run Services
```
docker compose up
```

### 4. Optional: Create Virtual Environment (Host)
If you are unable to use Docker, you can try this option to run the full project. Based on this, you need to create 2 individual venv for Frontend & Backend. There is no complexity here; you can run both individually. Enter the directory and build it.

For Linux:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
---

