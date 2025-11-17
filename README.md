# RAG-Based AI Tutor With Images

Small, fully local demo of a Retrieval-Augmented Generation (RAG) tutor that can ingest a chapter PDF, answer follow-up questions, and surface the most relevant diagram in-line with every answer.

## Project Layout
- `backend/`: FastAPI service that handles PDF ingestion, chunking, TF-IDF embeddings, FAISS vector storage, grounded answer generation, and image retrieval.
- `frontend/`: Vite + React single-page app with PDF upload, chat interface, and inline image rendering.
- `backend/data/`: Persisted PDFs, FAISS indices, metadata JSON, and the provided diagram assets.

## Prerequisites
- Python 3.12+
- Node.js 18+ (with npm)
- macOS/Linux shell (tested on macOS 15)

## Backend Setup
```bash
cd /Users/sk__volley__07/Desktop/New\ Beginning/Assignment_Edulevel/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API becomes available at `http://localhost:8000`. Static diagrams are automatically served from `/static/images/<filename>`.

## Frontend Setup
```bash
cd /Users/sk__volley__07/Desktop/New\ Beginning/Assignment_Edulevel/frontend
npm install
npm run dev -- --host
```

Visit the Vite dev server URL (printed in the console) and upload a PDF to start chatting.

## Key API Endpoints
- `POST /api/v1/upload`
  - Body: multipart form with a `file` field (PDF).
  - Response: `{ "topic_id": "...", "message": "...", "chunks_processed": 42 }`
- `POST /api/v1/chat`
  - Body: `{ "topic_id": "...", "question": "Explain echoes" }`
  - Response: grounded answer, supporting chunks, and an image filename/title.
- `GET /api/v1/images/{topic_id}`
  - Returns the diagram metadata for the topic (id, filename, title, keywords, description).
- `GET /static/images/<filename>`
  - Serves the actual PNG assets referenced by the chat responses.

## RAG Pipeline
1. **PDF → Text**: PyPDF2 extracts raw text, which is chunked with configurable size/overlap.
2. **Chunk Embeddings**: A namespace-aware TF-IDF vectorizer (scikit-learn) transforms chunk text into vectors.
3. **Vector Store**: FAISS FlatL2 index per topic stores chunk vectors plus metadata JSON for later retrieval.
4. **Retrieval**: On each question, we embed the query with the same vectorizer and look up the top-k chunks.
5. **Grounded Answering**: `LLMService` deterministically stitches together supporting sentences from the retrieved chunks, ensuring every statement is cited (`Source 1`, `Source 2`, ...).

## Image Retrieval Logic
- Each topic gets a JSON file with 6 curated diagrams (id, filename, title, keywords, description).
- A dedicated TF-IDF namespace embeds image metadata so the embedding space stays independent from chunk embeddings.
- When the tutor replies, it embeds the user question in the image namespace, ranks all diagrams via cosine similarity, and attaches the best match (title + filename). The frontend requests the PNG via `/static/images/<filename>`.

## Prompt / Response Template
The lightweight responder inside `app/services/llm_service.py` follows this template:
1. Extract sentences from each retrieved chunk that overlap with the user question keywords.
2. Trim/shorten sentences for readability.
3. Build the final message:
   ```
   Here is what I found in the uploaded chapter regarding "<question>":
   - Source 1: <sentence>
   - Source 2: <sentence>

   These statements are quoted directly from the retrieved study material...
   ```
This keeps answers grounded even without an external LLM key.

## Demo Video
Record a 2–4 minute screen capture that shows:
1. Starting the FastAPI and Vite dev servers.
2. Uploading the provided sound chapter PDF.
3. Asking a few questions and pointing out the inline diagrams.
4. Mentioning where the README explains the pipeline.

Any screen recorder (QuickTime, OBS, etc.) works for the deliverable.

