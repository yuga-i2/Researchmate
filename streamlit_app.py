import streamlit as st
from src.vectorstore import VectorStore

# Initialize vectorstore
vs = VectorStore()

st.title("ResearchMate - Semantic Paper Search")

# Input query
query = st.text_input("Enter your search query:")

if query:
    results = vs.search(query)
    if results:
        st.write(f"Found {len(results)} results:")
        for hit in results:
            st.subheader(hit['metadata'].get('title', 'Untitled'))
            st.write(hit['document'][:500] + "...")  # show first 500 chars
            st.write(f"Distance: {hit['distance']:.4f}")
    else:
        st.write("No results found.")
