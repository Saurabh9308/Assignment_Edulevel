import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

router = APIRouter()
rag_pipeline = RAGPipeline()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(request: ChatRequest):
    """
    Send a question to the AI tutor and get a response with relevant image
    """
    try:
        logger.info("Chat request | topic=%s question='%s'", request.topic_id, request.question)
        
        # Process the question through RAG pipeline
        result = rag_pipeline.process_query(request.topic_id, request.question)
        
        logger.info(
            "RAG pipeline completed | answer_len=%s chunks=%s image=%s",
            len(result["answer"]),
            len(result["relevant_chunks"]),
            result["image_filename"],
        )
        
        return ChatResponse(
            answer=result["answer"],
            relevant_chunks=result["relevant_chunks"],
            image_id=result["image_id"],
            image_filename=result["image_filename"],
            image_title=result["image_title"]
        )
        
    except Exception as e:
        logger.exception("Error in chat endpoint: %s", e)
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")