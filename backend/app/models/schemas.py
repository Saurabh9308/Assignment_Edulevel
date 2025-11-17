from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class UploadResponse(BaseModel):
    topic_id: str
    message: str
    chunks_processed: int

class ChatRequest(BaseModel):
    topic_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    relevant_chunks: List[str]
    image_id: Optional[str] = None
    image_filename: Optional[str] = None
    image_title: Optional[str] = None

class ImageMetadata(BaseModel):
    id: str
    filename: str
    title: str
    keywords: List[str]
    description: str

class TopicImagesResponse(BaseModel):
    topic_id: str
    images: List[ImageMetadata]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None