from typing import List
import re
from textwrap import shorten
from app.core.config import settings

class LLMService:
    """
    Lightweight, deterministic response generator that grounds answers
    directly in the retrieved PDF chunks. This is not a real LLM but
    it keeps the pipeline functional without requiring API keys.
    """
    def __init__(self):
        self.model_name = settings.LLM_MODEL
    
    def _extract_supporting_sentences(self, question: str, chunk: str) -> List[str]:
        keywords = [word.lower() for word in re.findall(r"\b\w{4,}\b", question)]
        sentences = re.split(r"(?<=[.!?])\s+", chunk.strip())
        matches = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                matches.append(sentence.strip())
        if not matches:
            matches = sentences[:2]
        return [shorten(sentence, width=260, placeholder="...") for sentence in matches if sentence]
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Compose a grounded explanation pulled only from the retrieved PDF text.
        """
        if not context_chunks:
            return "I could not find relevant information about that in the uploaded chapter."
        
        collected_sentences = []
        for idx, chunk in enumerate(context_chunks):
            sentences = self._extract_supporting_sentences(question, chunk)
            for sentence in sentences:
                collected_sentences.append((idx + 1, sentence))
                if len(collected_sentences) >= 6:
                    break
            if len(collected_sentences) >= 6:
                break
        
        if not collected_sentences:
            collected_sentences.append((1, shorten(context_chunks[0], width=260, placeholder="...")))
        
        plain_sentences = [sentence for _, sentence in collected_sentences]
        explanation = " ".join(plain_sentences).strip()
        if not explanation:
            explanation = shorten(context_chunks[0], width=260, placeholder="...")
        
        citations = "\n".join(
            f"- Source {source_id}: {sentence}"
            for source_id, sentence in collected_sentences[:4]
        )
        
        answer = (
            f'Here’s a summary from the uploaded chapter about "{question}":\n\n'
            f"{explanation}\n\n"
            "Supporting excerpts from the PDF:\n"
            f"{citations}"
        )
        return answer
    
    def is_available(self) -> bool:
        return False