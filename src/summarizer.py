"""
summarizer.py — ResearchMate Gemini-powered summarizer
-------------------------------------------------------

This module handles interaction with Google's Gemini API to summarize and synthesize
research paper content.

✅ Requirements:
    pip install google-generativeai python-dotenv

✅ Setup:
    1. Create a .env file in your project root with:
        GEMINI_API_KEY=your_gemini_api_key_here
        GEMINI_MODEL=gemini-1.5-flash   # or gemini-1.5-pro if you prefer
    2. Load environment before running:
        python -m src.app --q "Recent advances in diffusion models"
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env (if present)
load_dotenv()


def init_gemini():
    """Initialize and configure the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "❌ GEMINI_API_KEY not found. Please set it in your environment or .env file."
        )
    genai.configure(api_key=api_key)

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name)
    return model


# Initialize Gemini model globally (so it's loaded only once)
model = init_gemini()


def make_summary_prompt(query: str, context: str) -> str:
    """
    Create a structured prompt instructing Gemini to summarize and synthesize
    research findings from provided paper contexts.
    """
    prompt = f"""
You are an expert AI research assistant specializing in analyzing and summarizing scientific papers.

Your task:
1. Write a **concise 3–5 sentence synthesis** of the current state of research for the topic.
2. Provide **five bullet-point insights** or findings with short reasoning or citations.
3. Suggest **three future research directions** or open challenges.
4. Mention any **conflicting results** or unclear conclusions if found.

Be factual, avoid hallucinations, and indicate uncertainty if the context lacks evidence.

---

**Query / Topic:** {query}

**Context (from papers):**
{context}

---

Format your answer clearly using Markdown headings.
"""
    return prompt


def summarize_topic(query: str, context: str, max_tokens: int = 1000) -> str:
    """
    Generate a Gemini-powered summary for the given research query and context.
    """
    prompt = make_summary_prompt(query, context)

    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text.strip()
        elif isinstance(response, str):
            return response.strip()
        else:
            return "[No valid text output returned by Gemini API.]"
    except Exception as e:
        return f"[Gemini API Error] {str(e)}"
