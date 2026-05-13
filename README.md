````md
# Medical RAG Assistant

A local AI-powered Medical RAG Assistant that allows users to upload medical PDF documents and ask questions based on the uploaded content using Retrieval-Augmented Generation (RAG).

The system extracts text from PDFs, converts the content into embeddings, stores them in a vector database, retrieves relevant medical context, and generates responses using Llama3 through Ollama.

---

## Features

- Medical PDF upload and ingestion
- PDF text extraction
- Intelligent text chunking with overlap
- SentenceTransformer embeddings
- ChromaDB vector database
- Semantic similarity search
- Local Llama3 inference using Ollama
- FastAPI backend APIs
- Swagger API documentation
- Streamlit frontend interface
- Retrieval-based question answering

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### AI / RAG
- SentenceTransformers
- ChromaDB
- Ollama
- Llama3

### Frontend
- Streamlit

### Utilities
- pypdf
- requests
- python-dotenv

---

## Architecture

```text
User uploads PDF
        ↓
FastAPI Backend receives file
        ↓
PDF text extraction using pypdf
        ↓
Text is split into chunks
        ↓
Chunks are converted into embeddings
        ↓
Embeddings are stored in ChromaDB
        ↓
User asks a question
        ↓
Question is converted into embedding
        ↓
ChromaDB retrieves similar chunks
        ↓
Retrieved context is sent to Llama3/Ollama
        ↓
Final answer is returned to user
```

---

## Project Structure

```text
medical-rag-assistant/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── ask.py
│   │   │   ├── ingest.py
│   │   │   └── health.py
│   │   │
│   │   ├── schemas/
│   │   │   └── chat.py
│   │   │
│   │   └── services/
│   │       ├── pdf_loader.py
│   │       ├── document_loader.py
│   │       ├── embedding_service.py
│   │       └── vector_store.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app.py
│
├── chroma_db/
│
├── README.md
└── .gitignore
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Checks whether the backend server is running.

---

### Upload PDF

```http
POST /ingest-pdf
```

Uploads and ingests medical PDF documents into the vector database.

---

### Ask Question

```http
POST /ask
```

Accepts a medical question, retrieves relevant document chunks, and generates a response using Llama3.

---

## Swagger API Documentation

After running the backend server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows testing all APIs directly from the browser.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/shivanisindhe3/medical-rag-assistant.git
cd medical-rag-assistant
```

---

## Backend Setup

```bash
cd backend

pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

pip install streamlit requests
```

---

## Run Frontend

```bash
streamlit run app.py
```

---

## Example Workflow

1. Start backend server
2. Open Swagger documentation
3. Upload a medical PDF using `/ingest-pdf`
4. Ask medical questions using `/ask`
5. System retrieves relevant context
6. Llama3 generates final response

---

## Future Improvements

- Multi-PDF support
- Chat history memory
- Source citation display
- Better chunking strategies
- Authentication system
- Docker deployment
- Cloud deployment
- Admin dashboard
- Medical report summarization
- OCR support for scanned PDFs

---

## Disclaimer

This project is developed for educational and research purposes only.

The system is not intended to replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical concerns.

---

## Author

Shivani Sindhe

GitHub:
[medical-rag-assistant repository](https://github.com/shivanisindhe3/medical-rag-assistant)
````
