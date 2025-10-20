"""
embeddings.py — Generate embeddings for text using Gemini
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np

# Load .env variables
load_dotenv()

# Initialize Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment or .env file")
genai.configure(api_key=api_key)

# Default model for embeddings
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")


def get_embeddings(texts):
    """
    Returns a numeric embedding vector for a single string, 
    or a list of vectors for a list of strings.
    Ensures 1D vectors for single string.
    """
    single_input = False
    if isinstance(texts, str):
        texts = [texts]
        single_input = True

    embeddings = []
    for text in texts:
        if not text:
            embeddings.append(np.zeros(768).tolist())  # fallback vector
            continue
        try:
            response = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=text
            )
            embeddings.append(response["embedding"])
        except Exception as e:
            print(f"[Gemini Embedding Error] {e}")
            embeddings.append(np.zeros(768).tolist())

    return embeddings[0] if single_input else embeddings
