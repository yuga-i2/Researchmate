"""
embedder.py — Handles text embeddings for ResearchMate
"""

import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("researchmate.embedder")

# Initialize a transformer model for embedding (you can change model if needed)
# 'all-MiniLM-L6-v2' is small, fast, and works great for semantic search
_model = None


def get_model():
    global _model
    if _model is None:
        logger.info("Loading embedding model: all-MiniLM-L6-v2")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embeddings(text: str) -> List[float]:
    """
    Converts text into an embedding vector.
    Returns an empty list if text is invalid or embedding fails.
    """
    try:
        text = text.strip()
        if not text:
            return []
        model = get_model()
        embedding = model.encode(text, convert_to_numpy=True).tolist()
        return embedding
    except Exception as e:
        logger.warning(f"Embedding failed: {e}")
        return []
