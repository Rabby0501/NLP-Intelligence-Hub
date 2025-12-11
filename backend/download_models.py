import os
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoProcessor,
)
from sentence_transformers import SentenceTransformer
from transformers import BlipForConditionalGeneration

BASE_DIR = os.path.join(os.path.dirname(__file__), "models")

SENTIMENT_DIR = os.path.join(BASE_DIR, "sentiment")
EMBED_DIR = os.path.join(BASE_DIR, "embedder")
SUMMARY_DIR = os.path.join(BASE_DIR, "summarizer")
BLIP_DIR = os.path.join(BASE_DIR, "blip")

os.makedirs(SENTIMENT_DIR, exist_ok=True)
os.makedirs(EMBED_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)
os.makedirs(BLIP_DIR, exist_ok=True)

print("=== Downloading SENTIMENT model (DistilBERT) ===")
sent_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
sent_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
sent_tokenizer.save_pretrained(SENTIMENT_DIR)
sent_model.save_pretrained(SENTIMENT_DIR)
print("Saved sentiment model to", SENTIMENT_DIR)

print("=== Downloading EMBEDDING model (MiniLM) ===")
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embed_model.save(EMBED_DIR)
print("Saved embedding model to", EMBED_DIR)

print("=== Downloading SUMMARIZER model (DistilBART) ===")
sum_tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
sum_model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
sum_tokenizer.save_pretrained(SUMMARY_DIR)
sum_model.save_pretrained(SUMMARY_DIR)
print("Saved summarizer model to", SUMMARY_DIR)

print("=== Downloading BLIP image caption model ===")
blip_processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
blip_processor.save_pretrained(BLIP_DIR)
blip_model.save_pretrained(BLIP_DIR)
print("Saved BLIP model to", BLIP_DIR)

print("✅ All models downloaded and saved locally.")
