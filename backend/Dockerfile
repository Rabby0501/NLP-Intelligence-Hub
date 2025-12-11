FROM python:3.11-slim

WORKDIR /app

# System deps (optional, but useful for Pillow etc.)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --timeout 600 -r requirements.txt

# Copy local models (downloaded earlier on host)
COPY models /app/models

# Set env so nlp_utils.py knows where models are
ENV MODEL_DIR=/app/models


# Copy FastAPI app
COPY app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

