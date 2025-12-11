from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from .nlp_utils import get_or_create_collection, add_document

 
from .models import (
    TextRequest,
    SentimentResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
    SummaryResponse,
    ImageCaptionResponse,
)

from .nlp_utils import (
    get_or_create_collection,
    analyze_sentiment,
    semantic_search,
    summarize_text,
    caption_image,
    ensure_sample_data_loaded,
    add_document
    
)

app = FastAPI(
    title="NLP Intelligence Hub API",
    description="A multi-model NLP backend supporting sentiment analysis, semantic search, QA, summarization, image captioning, and ChromaDB.",
    version="1.2.0",
)

# CORS for Streamlit frontend
origins = ["*"]  # you can restrict later

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Make sure Chroma has sample docs
    ensure_sample_data_loaded()

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

# ---------------- SENTIMENT ----------------
@app.post("/sentiment", response_model=SentimentResponse, tags=["NLP Processing"])
def sentiment(req: TextRequest):
    add_document(req.text, doc_type="sentiment_input")
    
    label, score = analyze_sentiment(req.text)
    return SentimentResponse(label=label, score=score)


# ---------------- SEMANTIC SEARCH ----------------
@app.post("/semantic-search", response_model=SearchResponse, tags=["NLP Processing"])
def search(req: SearchRequest):
    add_document(req.query, doc_type="semantic_search_query")

    raw_results = semantic_search(req.query, top_k=req.top_k)
    results = [
        SearchResult(id=r["id"], text=r["text"], score=r["score"])
        for r in raw_results
    ]

    return SearchResponse(results=results)


# ---------------- SUMMARIZER ----------------
@app.post("/summarize", response_model=SummaryResponse, tags=["NLP Processing"])
def summarize(req: TextRequest):

    # LOG text before summarizing
    add_document(req.text, doc_type="summary_input")

    summary = summarize_text(req.text)

    # LOG summary output
    add_document(summary, doc_type="summary_output")

    return SummaryResponse(summary=summary)


# ---------------- IMAGE CAPTION ----------------
@app.post("/image-caption", response_model=ImageCaptionResponse, tags=["NLP Processing"])
async def image_caption(file: UploadFile = File(...)):

    image_bytes = await file.read()
    caption = caption_image(image_bytes)

    # LOG the generated caption
    add_document(caption, doc_type="image_caption_result")

    return ImageCaptionResponse(caption=caption)


# ---------------- CHROMA INFO ----------------
@app.get("/chroma-info", tags=["Database Management"])
def chroma_info():
    try:
        col = get_or_create_collection()
        data = col.get()

        organized = []
        for i in range(len(data["ids"])):
            organized.append({
                "id": data["ids"][i],
                "text": data["documents"][i],
                "metadata": data["metadatas"][i]
            })

        return {
            "collection_name": col.name,
            "document_count": col.count(),
            "documents": organized,
        }
    except Exception as e:
        return {"error": str(e)}

