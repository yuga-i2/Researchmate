<h1 align="center">🧠 ResearchMate</h1>
<h3 align="center">AI-Powered Research Assistant for Intelligent Paper Discovery & Summarization</h3>

---

## 🚀 Overview
**ResearchMate** is a lightweight AI system that automatically **collects, embeds, and searches scientific papers** using semantic search.  
It helps researchers and students quickly find relevant papers and insights — powered by **Gemini API**, **ChromaDB**, and **Streamlit**.

---

## ⚙️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend** | Python + FastAPI / ChromaDB / SQLite |
| **Frontend** | Streamlit |
| **LLM** | Gemini API (default) / Ollama (optional) |
| **Vector Store** | ChromaDB (default) / FAISS (fallback) |
| **Data Sources** | arXiv + Semantic Scholar |

---

## 🗂️ Folder Structure

```plaintext
ResearchMate/
│
├── src/                    # Core application logic
│   ├── app.py              # Main CLI entrypoint
│   ├── collector.py        # Fetches papers from arXiv / Semantic Scholar
│   ├── embedder.py         # Handles text embeddings via Gemini API
│   ├── vectorstore.py      # ChromaDB storage & semantic search
│   └── utils.py            # Helper utilities
│
├── data/                   # (Optional) Downloaded paper data
├── chroma_db/              # Local Chroma database files
├── notebooks/              # Jupyter demos / experiments
├── streamlit_app.py        # Streamlit web interface
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Files ignored by Git
└── README.md

---

