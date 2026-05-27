import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import psycopg2
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "document_chunks") # Mantém o nome da coleção
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_document(path: str):
    """Carrega o documento PDF do caminho especificado."""
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo PDF não encontrado em: {path}")
    
    print(f"Carregando PDF de: {path}")
    loader = PyPDFLoader(path)
    return loader.load()

def split_documents(documents: list):
    """Divide os documentos em chunks de 1000 caracteres com overlap de 150."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)
    print(f"PDF dividido em {len(chunks)} chunks.")
    return chunks

def get_embedding_engine():
    """Inicializa o serviço de embeddings do Google Generative AI."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY não encontrada. Verifique seu arquivo .env")
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

def persist_data(chunks: list, embeddings):
    """Salva os chunks no banco de dados vetorial com controle de cota (batching)."""
    # Limpeza profunda: Removemos as tabelas para evitar conflitos de schema entre versões
    print(f"Limpando schema e dados existentes...")
    # Removemos o prefixo '+psycopg2' da URL para o driver psycopg2 puro
    db_url = CONNECTION_STRING.replace("+psycopg2", "")
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            # Remove as tabelas padrão do LangChain Postgres se existirem
            cur.execute("DROP TABLE IF EXISTS langchain_pg_embedding CASCADE;")
            cur.execute("DROP TABLE IF EXISTS langchain_pg_collection CASCADE;")
        conn.commit()

    print("Iniciando persistência no banco de dados...")
    
    # Usamos batching para evitar o erro 429 RESOURCE_EXHAUSTED
    batch_size = 5
    with tqdm(total=len(chunks), desc="Processando Chunks") as pbar:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            PGVector.from_documents(
                embedding=embeddings,
                documents=batch,
                collection_name=COLLECTION_NAME,
                connection=CONNECTION_STRING,
                use_jsonb=True,
            )
            pbar.update(len(batch))
            time.sleep(6)  # Pausa de 6s para garantir no máximo 10 requisições por minuto (RPM) e respeitar o TPM

def ingest_pdf():
    """Fluxo principal de ingestão utilizando métodos coesos."""
    try:
        docs = load_document(PDF_PATH)
        chunks = split_documents(docs)
        embeddings = get_embedding_engine()
        persist_data(chunks, embeddings)
        print("Ingestão concluída com sucesso no banco de dados!")
    except Exception as e:
        print(f"Erro durante a ingestão: {e}")


if __name__ == "__main__":
    ingest_pdf()