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

```

## 🔑 Environment Variables
All API keys and configuration values are stored in a `.env` file (copy from `.env.example`).

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key. | `your-gemini-api-key-here` |
| `CHROMA_PATH` | Path to the local Chroma database directory. | `./chroma_db` |
| `DATA_DIR` | Directory to store paper data. | `./data` |

**Example `.env` file:**
```bash
# Google Gemini API Key
GEMINI_API_KEY=your-gemini-api-key-here

# Path to local Chroma database
CHROMA_PATH=./chroma_db

# Directory to store paper data
DATA_DIR=./data

```
## 🧠 System Workflow
### 🔍 Architecture Overview
The system uses a Vector Database workflow to power its semantic search capabilities:
flowchart TD
    A[User enters query in Streamlit UI] --> B[App sends query to ResearchMate backend]
    B --> C[Collector Module searches ArXiv & Semantic Scholar APIs]
    C --> D[Valid papers are processed & cleaned]
    D --> E[Embedder generates sentence embeddings using all-MiniLM-L6-v2]
    E --> F[Embeddings stored in Chroma Vector Database]
    F --> G[User runs query via UI or CLI]
    G --> H[VectorStore retrieves top matching papers]
    H --> I[Results displayed in Streamlit interface]


