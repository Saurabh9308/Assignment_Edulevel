## Backend Service

FastAPI application that powers the RAG-based AI Tutor. It ingests PDFs, builds TF-IDF embeddings, persists FAISS indices, and answers chat questions with grounded citations plus image recommendations.

### Tech Stack
- FastAPI + Uvicorn
- PyPDF2 for text extraction
- scikit-learn TF-IDF vectorizer
- FAISS (CPU) for similarity search
- Pillow + static file serving for diagram delivery

### Project Layout
```
app/
  api/               # Upload, chat, and images endpoints
  core/              # Settings + logging config
  services/          # PDF processing, embeddings, vector store, RAG, images, LLM stub
  utils/             # Shared helpers
data/
  pdfs/              # Uploaded PDFs (per topic)
  vectors/           # FAISS index + metadata per topic
  images/            # Static diagrams returned with answers
  metadata/          # Image metadata JSON per topic
```

### Running Locally
```bash
cd /Users/sk__volley__07/Desktop/New\ Beginning/Assignment_Edulevel/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### API Overview
- `POST /api/v1/upload`: accepts a PDF file, extracts chunks, builds embeddings, and returns a `topic_id`.
- `POST /api/v1/chat`: expects `{ "topic_id": "...", "question": "..." }` and responds with grounded text plus an image filename/title.
- `GET /api/v1/images/{topic_id}`: returns all diagram metadata for the topic.
- `GET /static/images/<filename>`: static route for diagram PNGs (consumed by the frontend).

### Logging
`app/core/logging_config.py` centralizes logging setup so every module can rely on `logging.getLogger(__name__)`. Run the server with `LOG_LEVEL=DEBUG` (environment variable) if you need more verbose traces.

