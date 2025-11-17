import logging
import os
import uuid
from typing import List, Dict, Any
import PyPDF2
from app.core.config import settings

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file
        """
        try:
            logger.info("Extracting text from %s", pdf_path)
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if PDF has pages
                if len(pdf_reader.pages) == 0:
                    raise Exception("PDF has no pages")
                
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text.strip():
                    raise Exception("No text could be extracted from the PDF")
                
                logger.info("Extracted %s characters from PDF", len(text))
                return text.strip()
                
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks for better retrieval
        """
        words = text.split()
        chunks = []
        chunk_id = 0
        
        i = 0
        while i < len(words):
            # Create chunk
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Create chunk metadata
            chunk_data = {
                "id": str(uuid.uuid4()),
                "chunk_id": chunk_id,
                "text": chunk_text,
                "word_count": len(chunk_words),
                "start_index": i,
                "end_index": min(i + self.chunk_size, len(words))
            }
            
            chunks.append(chunk_data)
            chunk_id += 1
            
            # Move forward, considering overlap
            i += (self.chunk_size - self.chunk_overlap)
        
        return chunks
    
    def process_pdf_from_path(self, pdf_path: str, topic_id: str) -> Dict[str, Any]:
        """
        Process PDF from file path: extract text and chunk it
        """
        try:
            # Verify file exists and has content
            if not os.path.exists(pdf_path):
                raise Exception(f"PDF file not found: {pdf_path}")
            
            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                raise Exception("PDF file is empty")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            return {
                "topic_id": topic_id,
                "pdf_path": pdf_path,
                "text_length": len(text),
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
            
        except Exception as e:
            # Clean up file if processing failed
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def process_pdf(self, pdf_file, topic_id: str) -> Dict[str, Any]:
        """
        Main method to process PDF: save, extract text, and chunk it
        """
        try:
            # Save PDF file
            pdf_filename = f"{topic_id}.pdf"
            pdf_path = os.path.join(settings.PDF_DIR, pdf_filename)
            
            # Save the file
            pdf_file.file.seek(0)  # Reset file pointer
            with open(pdf_path, "wb") as buffer:
                buffer.write(pdf_file.file.read())
            
            # Process from saved path
            return self.process_pdf_from_path(pdf_path, topic_id)
            
        except Exception as e:
            # Clean up file if processing failed
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise Exception(f"PDF processing failed: {str(e)}")