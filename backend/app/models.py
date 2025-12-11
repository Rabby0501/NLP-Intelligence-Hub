from pydantic import BaseModel
from typing import List, Optional

class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    score: float

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

class SummaryResponse(BaseModel):
    summary: str

class ImageCaptionResponse(BaseModel):
    caption: str
