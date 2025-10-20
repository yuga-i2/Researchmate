"""
vectorstore.py — Manages ChromaDB vector storage for ResearchMate
"""

import logging
import chromadb
from src.embedder import get_embeddings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        # Initialize Chroma persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Create or load collection
        self.collection_name = "researchmate_papers"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

        logger.info(f"Loaded existing collection: {self.collection_name}")

    def add_documents(self, documents, metadatas=None, ids=None):
        """
        Adds text documents to the vector store.
        """
        try:
            embeddings = [get_embeddings(doc) for doc in documents]

            # Ensure metadatas and ids are lists of same length
            if metadatas is None:
                metadatas = [{} for _ in documents]
            if ids is None:
                ids = [str(i) for i in range(len(documents))]

            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            logger.info(f"Added {len(documents)} documents to vectorstore.")
        except Exception as e:
            logger.error(f"Error adding documents to vectorstore: {e}")

    def search(self, query_text: str, top_k: int = 3):
        """
        Searches for the most similar documents to the given query.
        """
        try:
            query_embedding = get_embeddings(query_text)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            if not results or "documents" not in results:
                return []

            hits = []
            for i in range(len(results["documents"][0])):
                hits.append({
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                })
            return hits
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
