import logging
import os
import json
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, topic_id: str):
        self.topic_id = topic_id
        self.index = None
        self.chunks = []
        self.index_path = os.path.join(settings.VECTOR_DIR, f"{topic_id}.faiss")
        self.metadata_path = os.path.join(settings.VECTOR_DIR, f"{topic_id}_metadata.json")
    
    def create_index(self, embeddings: np.ndarray, chunks: List[Dict[str, Any]]):
        """
        Create FAISS index from embeddings and store chunks metadata
        """
        try:
            # Validate embeddings
            if len(embeddings) == 0:
                raise Exception("No embeddings provided")
            
            dimension = embeddings.shape[1]
            logger.info("Creating FAISS index with dimension %s", dimension)
            
            # Create FAISS index (L2 distance)
            self.index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to index
            self.index.add(embeddings.astype(np.float32))
            self.chunks = chunks
            
            logger.info("Created FAISS index with %s chunks, dimension %s", len(chunks), dimension)
            
        except Exception as e:
            raise Exception(f"Error creating FAISS index: {str(e)}")
    
    def save_index(self):
        """
        Save FAISS index and metadata to disk
        """
        try:
            if self.index is None:
                raise Exception("No index to save")
            
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)
            
            # Save metadata
            metadata = {
                "topic_id": self.topic_id,
                "chunks": self.chunks,
                "index_type": "FlatL2",
                "total_chunks": len(self.chunks),
                "dimension": self.index.d
            }
            
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info("Saved index and metadata for topic %s", self.topic_id)
            
        except Exception as e:
            raise Exception(f"Error saving index: {str(e)}")
    
    def load_index(self):
        """
        Load FAISS index and metadata from disk
        """
        try:
            if not os.path.exists(self.index_path):
                raise Exception(f"Index file not found: {self.index_path}")
            
            # Load FAISS index
            self.index = faiss.read_index(self.index_path)
            
            # Load metadata
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
                self.chunks = metadata["chunks"]
            
            logger.info("Loaded index with %s chunks, dimension %s", len(self.chunks), self.index.d)
            
        except Exception as e:
            raise Exception(f"Error loading index: {str(e)}")
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using FAISS
        """
        if self.index is None:
            self.load_index()
        
        try:
            # Validate query embedding dimensions
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            query_dim = query_embedding.shape[1]
            index_dim = self.index.d
            
            logger.debug("Query dimension: %s, Index dimension: %s", query_dim, index_dim)
            
            if query_dim != index_dim:
                raise Exception(f"Dimension mismatch: Query has {query_dim} dimensions, but index has {index_dim} dimensions")
            
            # Search in FAISS index
            distances, indices = self.index.search(query_embedding.astype(np.float32), k)
            
            # Get relevant chunks
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.chunks):
                    chunk_data = self.chunks[idx].copy()
                    chunk_data["similarity_score"] = float(1 / (1 + distance))  # Convert distance to similarity
                    chunk_data["distance"] = float(distance)
                    results.append(chunk_data)
            
            return results
            
        except Exception as e:
            raise Exception(f"Error searching index: {str(e)}")
    
    def exists(self) -> bool:
        """
        Check if index exists for this topic
        """
        return os.path.exists(self.index_path) and os.path.exists(self.metadata_path)