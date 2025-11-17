import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "RAG AI Tutor"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Model Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # File Paths
    DATA_DIR: str = "data"
    PDF_DIR: str = os.path.join(DATA_DIR, "pdfs")
    VECTOR_DIR: str = os.path.join(DATA_DIR, "vectors")
    IMAGE_DIR: str = os.path.join(DATA_DIR, "images")
    METADATA_DIR: str = os.path.join(DATA_DIR, "metadata")
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_CHUNKS: int = 3
    IMAGE_SIMILARITY_THRESHOLD: float = float(os.getenv("IMAGE_SIMILARITY_THRESHOLD", 0.25))
    
    # Create directories if they don't exist
    def __init__(self):
        os.makedirs(self.PDF_DIR, exist_ok=True)
        os.makedirs(self.VECTOR_DIR, exist_ok=True)
        os.makedirs(self.IMAGE_DIR, exist_ok=True)
        os.makedirs(self.METADATA_DIR, exist_ok=True)

settings = Settings()