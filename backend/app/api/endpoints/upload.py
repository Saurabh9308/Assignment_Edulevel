import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import aiofiles
from app.models.schemas import UploadResponse
from app.services.pdf_processor import PDFProcessor
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.image_service import ImageService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
pdf_processor = PDFProcessor()
embedding_service = EmbeddingService()
image_service = ImageService()

async def save_uploaded_file(file: UploadFile, destination: str):
    """Save uploaded file asynchronously in chunks and rewind the stream."""
    await file.seek(0)
    async with aiofiles.open(destination, 'wb') as buffer:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            await buffer.write(chunk)
    await file.seek(0)

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract chunks, generate embeddings, and persist a vector index.
    """
    pdf_path = None
    try:
        filename = file.filename or ""
        is_pdf_upload = (file.content_type or "").lower() in {"application/pdf", "application/x-pdf"}
        has_pdf_extension = filename.lower().endswith(".pdf")

        if not (is_pdf_upload or has_pdf_extension):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        topic_id = str(uuid.uuid4())
        pdf_filename = f"{topic_id}.pdf"
        pdf_path = os.path.join(settings.PDF_DIR, pdf_filename)
        
        await save_uploaded_file(file, pdf_path)
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            os.remove(pdf_path)
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        logger.info("PDF saved | path=%s size=%s bytes", pdf_path, file_size)
        
        # Extract text chunks
        result = pdf_processor.process_pdf_from_path(pdf_path, topic_id)
        chunk_texts = [chunk["text"] for chunk in result["chunks"]]
        if not chunk_texts:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")
        
        # Create embeddings + FAISS index
        embeddings = embedding_service.generate_embeddings(chunk_texts, namespace="chunks")
        vector_store = VectorStore(topic_id)
        vector_store.create_index(embeddings, result["chunks"])
        vector_store.save_index()
        
        # Prepare image metadata for this topic
        image_service.create_sample_images(topic_id)
        
        response = UploadResponse(
            topic_id=topic_id,
            message="PDF processed successfully. You can start chatting about it now.",
            chunks_processed=result["chunk_count"]
        )
        logger.info(
            "Upload complete | topic=%s chunks=%s", topic_id, result["chunk_count"]
        )
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
        logger.exception("Error processing PDF upload: %s", e)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")