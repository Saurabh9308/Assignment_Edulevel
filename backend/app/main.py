from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.endpoints import upload, chat, images

setup_logging()

app = FastAPI(
    title="RAG AI Tutor API",
    description="AI Tutor Chatbot with RAG and Image Retrieval",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve chapter diagrams so the frontend can render them inline
app.mount(
    "/static/images",
    StaticFiles(directory=settings.IMAGE_DIR),
    name="chapter-images",
)

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(images.router, prefix="/api/v1", tags=["images"])


@app.get("/")
async def root():
    return {"message": "RAG AI Tutor API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
