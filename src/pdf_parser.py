import os
import requests
from pathlib import Path
from PyPDF2 import PdfReader
import logging
import re

logger = logging.getLogger(__name__)

# Directory to save downloaded PDFs
DATA_DIR = Path(__file__).parent.parent / "data" / "papers"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name: str) -> str:
    """
    Sanitize filename to avoid invalid characters.
    """
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)

def download_pdf(pdf_url: str, paper_id: str) -> str | None:
    """
    Downloads a PDF if it does not exist and returns the local path.
    """
    if not pdf_url:
        logger.warning("No PDF URL provided")
        return None

    filename = sanitize_filename(f"{paper_id}.pdf")
    pdf_path = DATA_DIR / filename

    if pdf_path.exists():
        return str(pdf_path)

    try:
        response = requests.get(pdf_url, timeout=15)
        response.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Saved PDF: {pdf_path}")
        return str(pdf_path)
    except Exception as e:
        logger.warning(f"Failed to download PDF {pdf_url}: {e}")
        return None

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.warning(f"Failed to extract text from {pdf_path}: {e}")
        return ""

def parse_pdf(paper: dict) -> dict | None:
    """
    Downloads and extracts text from a paper dictionary with keys: id, pdf_url, title, authors.
    Returns a dictionary with text and cleaned metadata for Chroma ingestion.
    """
    pdf_path = download_pdf(paper.get("pdf_url"), paper.get("id"))
    if not pdf_path:
        return None

    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        logger.warning(f"No text extracted from PDF {pdf_path}")
        return None

    # Clean metadata
    metadata = {
        "title": paper.get("title", ""),
        "authors": ", ".join(paper.get("authors", [])) if isinstance(paper.get("authors"), list) else paper.get("authors", ""),
        "id": paper.get("id", "")
    }

    return {
        "text": text,
        "metadata": metadata
    }
