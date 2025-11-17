import logging
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from typing import Dict
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Shared TF-IDF embedding utility.
    Supports logical namespaces (e.g. `chunks`, `images`) so that
    we can experiment with different vocabularies without breaking
    previously stored indices.
    """
    _instance = None
    _vectorizers: Dict[str, TfidfVectorizer] = {}
    _vectorizer_paths: Dict[str, str] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance
    
    def _get_vectorizer_path(self, namespace: str) -> str:
        if namespace not in self._vectorizer_paths:
            filename = f"tfidf_{namespace}_vectorizer.pkl"
            self._vectorizer_paths[namespace] = os.path.join(settings.VECTOR_DIR, filename)
        return self._vectorizer_paths[namespace]
    
    def _get_or_create_vectorizer(self, namespace: str) -> TfidfVectorizer:
        if namespace in self._vectorizers:
            return self._vectorizers[namespace]
        
        vectorizer_path = self._get_vectorizer_path(namespace)
        try:
            if os.path.exists(vectorizer_path):
                with open(vectorizer_path, 'rb') as f:
                    vectorizer = pickle.load(f)
                logger.info("Loaded TF-IDF vectorizer for namespace '%s'", namespace)
            else:
                vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
                logger.info("Created TF-IDF vectorizer for namespace '%s'", namespace)
        except Exception as e:
            logger.exception("Error loading vectorizer '%s': %s", namespace, e)
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        self._vectorizers[namespace] = vectorizer
        return vectorizer
    
    def _save_vectorizer(self, namespace: str):
        """Persist a namespace-scoped vectorizer to disk."""
        try:
            vectorizer = self._vectorizers.get(namespace)
            if vectorizer is None:
                return
            
            path = self._get_vectorizer_path(namespace)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                pickle.dump(vectorizer, f)
            logger.info("Saved TF-IDF vectorizer for namespace '%s'", namespace)
        except Exception as e:
            logger.exception("Error saving vectorizer '%s': %s", namespace, e)
    
    def generate_embeddings(self, texts: list, namespace: str = "chunks") -> np.ndarray:
        """
        Generate TF-IDF embeddings for a list of texts in a namespace.
        The first call for a namespace will fit the vectorizer; subsequent
        calls reuse the learned vocabulary to keep dimensions stable.
        """
        if not texts:
            raise ValueError("No texts provided for embedding generation.")
        
        try:
            vectorizer = self._get_or_create_vectorizer(namespace)
            logger.info("Generating TF-IDF embeddings for %s texts (namespace='%s')", len(texts), namespace)
            
            if not hasattr(vectorizer, 'vocabulary_') or len(vectorizer.vocabulary_) == 0:
                embeddings = vectorizer.fit_transform(texts).toarray()
                self._save_vectorizer(namespace)
            else:
                embeddings = vectorizer.transform(texts).toarray()
            
            logger.info("Generated embeddings with shape %s (namespace='%s')", embeddings.shape, namespace)
            return embeddings
            
        except Exception as e:
            raise Exception(f"Error generating embeddings for namespace '{namespace}': {str(e)}")
    
    def generate_single_embedding(self, text: str, namespace: str = "chunks") -> np.ndarray:
        """
        Generate embedding for a single text using the namespace vectorizer.
        """
        try:
            vectorizer = self._get_or_create_vectorizer(namespace)
            if not hasattr(vectorizer, 'vocabulary_') or len(vectorizer.vocabulary_) == 0:
                raise Exception(f"Vectorizer for namespace '{namespace}' is not initialized. "
                                "Please index some content first.")
            
            embedding = vectorizer.transform([text]).toarray()
            return embedding[0]
            
        except Exception as e:
            raise Exception(f"Error generating single embedding for namespace '{namespace}': {str(e)}")
    
    def get_vocabulary_size(self, namespace: str = "chunks") -> int:
        """Get the vocabulary size for a namespace."""
        vectorizer = self._get_or_create_vectorizer(namespace)
        if vectorizer and hasattr(vectorizer, 'vocabulary_'):
            return len(vectorizer.vocabulary_)
        return 0