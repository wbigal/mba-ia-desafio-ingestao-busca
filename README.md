# Desafio MBA Engenharia de Software com IA - Full Cycle

## Como executar a solução com Docker Compose

Siga os passos abaixo para configurar o ambiente, realizar a ingestão dos dados e testar a busca.

### 1. Subir o Ambiente
O projeto utiliza PostgreSQL com a extensão `pgvector` e um serviço Python. Certifique-se de que o Docker e o Docker Compose estão instalados e execute:
```bash
docker-compose up -d --build
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes configurações (ajuste conforme necessário):
```env
GOOGLE_API_KEY=sua_chave_aqui
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rag
PDF_PATH=./seu_documento.pdf
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
GOOGLE_LLM_MODEL=gemini-3.1-flash-lite
PG_VECTOR_COLLECTION_NAME=document_chunks
```

### 3. Executar a Ingestão de Dados
Para carregar o PDF, dividi-lo em chunks de 1000 caracteres e salvar os embeddings no banco:
```bash
docker-compose run --rm app python src/ingest.py
```

### 4. Testar o Chat/Busca
Após a ingestão, você pode testar a recuperação de informações e o chat executando:
```bash
docker-compose run --rm app python src/chat.py
```