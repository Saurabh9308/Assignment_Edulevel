import logging
import os
from typing import List, Dict, Any, Optional
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.services.image_service import ImageService
from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
        self.image_service = ImageService()
    
    def process_query(self, topic_id: str, question: str) -> Dict[str, Any]:
        """
        Main RAG pipeline: retrieve relevant content and generate answer
        """
        try:
            logger.info("Starting RAG pipeline for topic %s", topic_id)
            
            # Load vector store for the topic
            vector_store = VectorStore(topic_id)
            if not vector_store.exists():
                raise Exception(f"No vector store found for topic: {topic_id}")
            
            logger.debug("Vector store exists, loading index...")
            vector_store.load_index()
            
            # Generate embedding for the question
            logger.debug("Generating question embedding")
            question_embedding = self.embedding_service.generate_single_embedding(question, namespace="chunks")
            logger.debug("Question embedding generated with shape %s", question_embedding.shape)
            
            # Retrieve relevant chunks
            logger.debug("Searching for relevant chunks")
            relevant_chunks = vector_store.search(question_embedding, k=settings.TOP_K_CHUNKS)
            logger.info("Found %s relevant chunks", len(relevant_chunks))
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find relevant information in the learning material to answer your question.",
                    "relevant_chunks": [],
                    "image_id": None,
                    "image_filename": None,
                    "image_title": None
                }
            
            # Extract chunk texts for LLM context
            chunk_texts = [chunk["text"] for chunk in relevant_chunks]
            logger.debug("Chunk lengths: %s", [len(text) for text in chunk_texts])
            
            # Generate answer using LLM
            logger.debug("Generating answer with LLM")
            answer = self.llm_service.generate_answer(question, chunk_texts)
            logger.info("LLM answer generated (%s characters)", len(answer))
            
            # Ensure image metadata is ready and find the best match
            logger.debug("Finding relevant image")
            relevant_images = self.image_service.find_relevant_image(topic_id, question, top_k=1)
            image_data = relevant_images[0] if relevant_images else None

            if image_data and image_data.get("similarity_score", 0) < settings.IMAGE_SIMILARITY_THRESHOLD:
                logger.debug(
                    "Discarding low-similarity image (score=%.3f, threshold=%.3f)",
                    image_data["similarity_score"],
                    settings.IMAGE_SIMILARITY_THRESHOLD,
                )
                image_data = None

            logger.info("Selected image: %s", image_data["title"] if image_data else "None")
            
            return {
                "answer": answer,
                "relevant_chunks": chunk_texts,
                "image_id": image_data["id"] if image_data else None,
                "image_filename": image_data["filename"] if image_data else None,
                "image_title": image_data["title"] if image_data else None
            }
            
        except Exception as e:
            logger.exception("RAG pipeline error: %s", e)
            raise Exception(f"RAG pipeline error: {str(e)}")
    
    def get_available_topics(self) -> List[str]:
        """
        Get list of available topics (for debugging)
        """
        topics = []
        vector_dir = settings.VECTOR_DIR
        
        if os.path.exists(vector_dir):
            for filename in os.listdir(vector_dir):
                if filename.endswith(".faiss"):
                    topic_id = filename.replace(".faiss", "")
                    topics.append(topic_id)
        
        return topics