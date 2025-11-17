import logging
import os
import json
from typing import List, Dict, Any, Optional
import numpy as np
from app.core.config import settings
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.images_metadata: List[Dict[str, Any]] = []
        self.image_embeddings_cache: Dict[str, np.ndarray] = {}
        self.current_topic_id: Optional[str] = None
    
    def create_sample_images(self, topic_id: str) -> List[Dict[str, Any]]:
        """
        Create or refresh the canonical list of diagrams for a topic.
        """
        sample_images = [
            {
                "id": "img_001",
                "filename": "SchoolBellVibration.png",
                "title": "School Bell Vibration",
                "keywords": ["bell", "vibration", "sound", "school", "waves", "diagram"],
                "description": "Diagram showing how a school bell vibrates to produce sound waves"
            },
            {
                "id": "img_002", 
                "filename": "CompressionAndRefraction.png",
                "title": "Sound Wave Compression and Rarefaction",
                "keywords": ["compression", "rarefaction", "sound", "waves", "propagation", "physics"],
                "description": "Diagram showing compression and rarefaction in sound wave propagation"
            },
            {
                "id": "img_003",
                "filename": "MusicalInstrumentsVibrationChart.png", 
                "title": "Musical Instruments Vibration Chart",
                "keywords": ["musical", "instruments", "vibration", "sitar", "flute", "drum", "chart"],
                "description": "Chart showing how different musical instruments produce sound through vibration"
            },
            {
                "id": "img_004",
                "filename": "ReflectionOfSound.png",
                "title": "Sound Reflection Experiment",
                "keywords": ["reflection", "sound", "experiment", "echo", "plywood", "wood"],
                "description": "Experimental setup demonstrating sound reflection using different materials"
            },
            {
                "id": "img_005",
                "filename": "VibrationOfRubberBand.png",
                "title": "Rubber Band Vibration",
                "keywords": ["rubber", "band", "vibration", "plucking", "sound", "stretched"],
                "description": "Diagram showing how plucking a stretched rubber band produces sound through vibration"
            },
            {
                "id": "img_006",
                "filename": "VocalCordsDiagram.png",
                "title": "Vocal Cords Diagram",
                "keywords": ["vocal", "cords", "diagram", "vibration", "air", "lungs", "voice"],
                "description": "Anatomical diagram showing how vocal cords vibrate to produce sound"
            }
        ]
        
        self.images_metadata = sample_images
        self.current_topic_id = topic_id
        self._save_metadata(topic_id)
        self._generate_image_embeddings(topic_id)
        return sample_images
    
    def _save_metadata(self, topic_id: str):
        metadata_path = os.path.join(settings.METADATA_DIR, f"{topic_id}_images.json")
        os.makedirs(settings.METADATA_DIR, exist_ok=True)
        metadata = {
            "topic_id": topic_id,
            "images": self.images_metadata,
            "total_images": len(self.images_metadata)
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info("Saved image metadata for topic %s", topic_id)
    
    def _generate_image_embeddings(self, topic_id: str):
        """
        Generate embeddings for the currently loaded topic images and cache them.
        """
        if not self.images_metadata:
            self.image_embeddings_cache.pop(topic_id, None)
            return
        
        try:
            image_texts = [
                f"{image['title']}. {image['description']}. Keywords: {', '.join(image['keywords'])}"
                for image in self.images_metadata
            ]
            embeddings = self.embedding_service.generate_embeddings(image_texts, namespace="images")
            self.image_embeddings_cache[topic_id] = embeddings
            logger.info("Generated embeddings for %s images (topic=%s)", len(image_texts), topic_id)
        except Exception as e:
            logger.exception("Error generating image embeddings for topic %s: %s", topic_id, e)
            self.image_embeddings_cache.pop(topic_id, None)
    
    def ensure_topic_images(self, topic_id: str) -> bool:
        """
        Ensure metadata and embeddings exist for a topic. Creates sample metadata if needed.
        """
        if self.current_topic_id == topic_id and topic_id in self.image_embeddings_cache:
            return True
        
        if not self.image_exists(topic_id):
            self.create_sample_images(topic_id)
            return True
        
        return self.load_images(topic_id)
    
    def load_images(self, topic_id: str) -> bool:
        try:
            metadata_path = os.path.join(settings.METADATA_DIR, f"{topic_id}_images.json")
            if not os.path.exists(metadata_path):
                logger.warning("No image metadata found for topic %s", topic_id)
                return False
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                self.images_metadata = metadata["images"]
            
            self.current_topic_id = topic_id
            self._generate_image_embeddings(topic_id)
            logger.info("Loaded %s images for topic %s", len(self.images_metadata), topic_id)
            return True
        except Exception as e:
            logger.exception("Error loading images for topic %s: %s", topic_id, e)
            return False
    
    def find_relevant_image(self, topic_id: str, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Find the most relevant image for a query using embedding similarity.
        """
        if not self.ensure_topic_images(topic_id):
            logger.error("Unable to prepare images for topic %s", topic_id)
            return []
        
        embeddings = self.image_embeddings_cache.get(topic_id)
        if embeddings is None or embeddings.size == 0:
            logger.warning("No cached image embeddings available for topic %s", topic_id)
            return []
        
        try:
            logger.info("Finding relevant image for query '%s' (topic=%s)", query, topic_id)
            query_embedding = self.embedding_service.generate_single_embedding(query, namespace="images")
            
            similarities = []
            for i, image_embedding in enumerate(embeddings):
                query_norm = np.linalg.norm(query_embedding)
                image_norm = np.linalg.norm(image_embedding)
                similarity = 0.0
                if query_norm != 0 and image_norm != 0:
                    similarity = float(np.dot(query_embedding, image_embedding) / (query_norm * image_norm))
                similarities.append((similarity, i))
            
            similarities.sort(key=lambda x: x[0], reverse=True)
            results = []
            for similarity, idx in similarities[:top_k]:
                if idx < len(self.images_metadata):
                    image_data = self.images_metadata[idx].copy()
                    image_data["similarity_score"] = similarity
                    results.append(image_data)
            
            logger.info("Found %s relevant images for topic %s", len(results), topic_id)
            return results
        except Exception as e:
            logger.exception("Error finding relevant image for topic %s: %s", topic_id, e)
            return []
    
    def get_all_images(self, topic_id: str) -> List[Dict[str, Any]]:
        """
        Return the cached image metadata for a topic, ensuring it is loaded.
        """
        if not self.ensure_topic_images(topic_id):
            return []
        return self.images_metadata
    
    def image_exists(self, topic_id: str) -> bool:
        metadata_path = os.path.join(settings.METADATA_DIR, f"{topic_id}_images.json")
        return os.path.exists(metadata_path)