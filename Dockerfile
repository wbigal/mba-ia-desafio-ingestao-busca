FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    langchain langchain-community "langchain-google-genai>=1.0.10" google-generativeai langchain-text-splitters pypdf psycopg2-binary "psycopg[binary]" langchain-postgres python-dotenv tqdm

COPY . .

CMD ["python", "src/chat.py"]