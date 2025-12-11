FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --timeout 600 -r requirements.txt

# COPY streamlit_app.py .
# COPY . /app/
COPY . .

EXPOSE 8501

ENV API_BASE_URL=http://backend:8000

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
