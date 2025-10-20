# Researchmate

Researchmate is a lightweight research assistant for fetching papers from arXiv and Semantic Scholar, extracting text from PDFs, creating embeddings, and performing RAG-style retrieval and summarization using LLMs.

Repository structure:

researchmate/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── papers/ # downloaded PDFs and extracted text
├── src/
│   ├── __init__.py
│   ├── app.py # CLI / main agent loop
│   ├── collector.py # arXiv & Semantic Scholar fetchers
│   ├── pdf_parser.py # PDF download & text extraction
│   ├── embeddings.py # embedding model wrapper
│   ├── vectorstore.py # wrapper for Chroma/FAISS
│   ├── retriever.py # RAG retrieval utilities
│   ├── summarizer.py # LLM prompt & summarization utilities
│   ├── utils.py # helper functions (logging, rate-limit handling)
│   └── streamlit_app.py # optional frontend
└── notebooks/
    └── quick_demo.ipynb
