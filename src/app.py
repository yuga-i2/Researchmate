import argparse
import logging
from src.collector import collect_papers
from src.vectorstore import VectorStore
from src.embedder import get_embeddings  # ✅ Use embedder.py

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_queries(queries, max_papers=5):
    """
    Ingest papers for a list of queries into Chroma vectorstore.
    """
    vs = VectorStore()  # Initialize vectorstore once

    for query in queries:
        logger.info(f"Starting ingestion for query: '{query}'")
        papers = collect_papers(query, max_results=max_papers)
        logger.info(f"Collected {len(papers)} papers for query '{query}'")

        # Prepare valid papers (text -> abstract -> title)
        valid_papers = []
        for p in papers:
            text = p.get("text") or p.get("abstract") or p.get("title") or ""
            if isinstance(text, list):
                text = " ".join(text)  # flatten list if needed
            text = text.strip()
            if text:
                p["text_to_embed"] = text
                valid_papers.append(p)

        logger.info(f"Found {len(valid_papers)} valid papers with text/abstract/title")
        if not valid_papers:
            logger.warning("No valid papers to embed.")
            continue

        texts = [p["text_to_embed"] for p in valid_papers]
        metadatas = [{"title": p.get("title", "No Title"), "url": p.get("url", "No URL")} for p in valid_papers]
        ids = [f"{query}_{i}" for i in range(len(texts))]

        # Add to vectorstore (add_documents internally calls embedder)
        vs.add_documents(texts, metadatas, ids=ids)
        logger.info(f"Ingested {len(valid_papers)} papers for '{query}'")

def query_vectorstore(query, top_k=3):
    """
    Search the vectorstore for a query and print top results.
    """
    logger.info(f"Querying vectorstore for: {query}")
    vs = VectorStore()
    results = vs.search(query, top_k=top_k)

    if not results:
        print("⚠️ No results found.")
        return

    print(f"\n🔍 Top {len(results)} results for: '{query}'\n")
    for i, r in enumerate(results, start=1):
        title = r["metadata"].get("title", "No Title")
        url = r["metadata"].get("url", "No URL")
        print(f"{i}. {title}\n   🔗 {url}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ingest", "query"], required=True)
    parser.add_argument("--queries", nargs="+", help="Queries for ingestion mode")
    parser.add_argument("--query", help="Single query for search mode")
    parser.add_argument("--max", type=int, default=5)
    args = parser.parse_args()

    if args.mode == "ingest":
        if not args.queries:
            raise ValueError("You must provide --queries for ingest mode.")
        ingest_queries(args.queries, max_papers=args.max)
    elif args.mode == "query":
        if not args.query:
            raise ValueError("You must provide --query for query mode.")
        query_vectorstore(args.query)

if __name__ == "__main__":
    main()
