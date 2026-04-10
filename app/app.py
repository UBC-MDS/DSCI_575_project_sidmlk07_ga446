import sys
import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_pickle
from src.bm25 import bm25_search, load_bm25
from src.semantic import semantic_search, load_embeddings
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Amazon Product Search", page_icon="🔍", layout="wide")
st.title("🔍 Amazon Product Search")
st.caption("Milestone 1 — BM25 & Semantic Retrieval")


@st.cache_resource
def load_everything():
    corpus = load_pickle("data/processed/corpus.pkl")
    bm25, _ = load_bm25("data/processed/index")
    embeddings = load_embeddings("data/processed/index")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return corpus, bm25, embeddings, model


corpus, bm25, embeddings, model = load_everything()

st.sidebar.header("Search Settings")
method = st.sidebar.radio("Retrieval Method", ["BM25", "Semantic", "Both"])
top_k = st.sidebar.slider("Results to show", 1, 10, 5)

query = st.text_input("Enter your search query", placeholder="e.g. moisturizer for dry skin")


def show_results(results: list[dict], label: str):
    st.subheader(label)
    if not results:
        st.warning("No results found.")
        return
    for r in results:
        with st.container():
            st.markdown(f"**{r['rank']}. {r.get('title', 'No title')[:100]}**")
            col1, col2 = st.columns([3, 1])
            with col1:
                preview = (r.get("review_text") or "")[:200]
                st.write(f"_{preview}..._" if preview else "_No review text_")
            with col2:
                st.metric("Rating", f"{r.get('rating', 'N/A')}")
                st.metric("Score", f"{r['score']:.4f}")
            st.divider()


if query:
    if method in ("BM25", "Both"):
        results = bm25_search(query, bm25, corpus, top_k=top_k)
        show_results(results, "BM25 Results")

    if method in ("Semantic", "Both"):
        results = semantic_search(query, model, embeddings, corpus, top_k=top_k)
        show_results(results, "Semantic Results")
else:
    st.info("Type a query above to get started.")