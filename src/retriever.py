"""
Retriever module for ResearchMate.

Provides functionality to retrieve top-k most relevant document chunks
from the Chroma-backed vector store using embeddings.
"""

from typing import List, Tuple
import numpy as np

from .vectorstore import VectorStore
from .embeddings import get_embedding

class Retriever:
    """Retrieves relevant document chunks from the VectorStore."""

    def __init__(self, vectorstore: VectorStore = None):
        # Use existing VectorStore or initialize a new one
        self.vs = vectorstore or VectorStore()

    def retrieve(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Retrieve top-k documents for a given query.

        Returns a list of tuples: [(document_text, similarity_score), ...]
        """
        # Step 1: Embed the query
        query_emb = get_embedding(query)

        # Step 2: Query the vector store
        results = self.vs.query(query_emb, n_results=k)

        # Chroma returns dict with 'documents', 'metadatas', 'distances', 'ids'
        docs = results.get("documents", [[]])[0]  # results are nested list
        distances = results.get("distances", [[]])[0]

        # Step 3: Combine docs and distances
        retrieved = []
        for doc, dist in zip(docs, distances):
            # Convert distance to similarity if needed (optional)
            similarity = 1.0 / (1.0 + dist)  # simple transformation
            retrieved.append((doc, similarity))

        return retrieved

    def retrieve_text(self, query: str, k: int = 5) -> str:
        """
        Convenience method: returns concatenated top-k documents as a single string.
        Useful for feeding to the summarizer.
        """
        docs = self.retrieve(query, k)
        return "\n\n".join([doc for doc, _ in docs])
