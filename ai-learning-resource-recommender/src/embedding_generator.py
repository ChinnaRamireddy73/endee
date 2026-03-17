from sentence_transformers import SentenceTransformer
from src.config import MODEL_NAME
import torch

class EmbeddingGenerator:
    def __init__(self):
        print(f"Loading Embedding Model: {MODEL_NAME}...")
        try:
            self.model = SentenceTransformer(MODEL_NAME)
        except Exception as e:
            raise RuntimeError(f"Failed to load sentence-transformers model '{MODEL_NAME}'. Error: {e}")

    def generate(self, texts: list[str]) -> list[list[float]]:
        """
        Generates dense vector embeddings for a list of strings
        """
        if not texts:
            return []
            
        try:
            # Generate embeddings and convert to list of floats
            embeddings = self.model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {e}")
            
    def generate_single(self, text: str) -> list[float]:
        """
        Generate embedding for a single string query
        """
        return self.generate([text])[0]
