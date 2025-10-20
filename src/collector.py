"""
collector.py — Collect research papers from arXiv & Semantic Scholar
"""

import feedparser
import requests
import urllib.parse
import logging
from typing import List, Dict

logger = logging.getLogger("src.collector")

# --- Helper: Search arXiv ---
def search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    logger.info(f"Searching arXiv for query: '{query}'")

    base_url = "http://export.arxiv.org/api/query"
    encoded_query = urllib.parse.quote(query)
    url = f"{base_url}?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    feed = feedparser.parse(url)
    papers = []

    for entry in feed.entries:
        pdf_url = None
        for link in entry.links:
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                pdf_url = link.get("href")
                break

        papers.append({
            "id": entry.get("id", "")[-10:],
            "title": entry.get("title", "No title"),
            "authors": ", ".join(a.name for a in entry.authors),
            "pdf_url": pdf_url
        })

    return papers


# --- Helper: Search Semantic Scholar ---
def search_semantic_scholar(query: str, max_results: int = 5) -> List[Dict]:
    logger.info(f"Searching Semantic Scholar for query: '{query}'")

    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,url,isOpenAccess,openAccessPdf"
    }

    papers = []
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for paper in data.get("data", []):
                pdf_url = paper.get("openAccessPdf", {}).get("url")
                papers.append({
                    "id": paper.get("paperId"),
                    "title": paper.get("title"),
                    "authors": ", ".join(a["name"] for a in paper.get("authors", [])),
                    "pdf_url": pdf_url
                })
    except Exception as e:
        logger.warning(f"Semantic Scholar fetch failed: {e}")

    return papers


# --- Main Function ---
def collect_papers(query: str, max_results: int = 5) -> List[Dict]:
    """
    Collect papers from arXiv and Semantic Scholar for a given query.
    """
    arxiv_papers = search_arxiv(query, max_results)
    semantic_papers = search_semantic_scholar(query, max_results)
    all_papers = arxiv_papers + semantic_papers

    logger.info(f"Collected {len(all_papers)} papers for query '{query}'")
    return all_papers
