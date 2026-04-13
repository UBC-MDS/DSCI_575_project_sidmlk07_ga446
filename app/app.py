import sys
import streamlit as st
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_corpus_parquet, load_pickle
from src.bm25 import bm25_search, load_bm25
from src.semantic import semantic_search, load_semantic_artifacts
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Amazon Product Search", page_icon="🔍", layout="wide")
st.title("🔍 Amazon Product Search")
st.caption("Milestone 1 — BM25 & Semantic Retrieval")


@st.cache_resource
def load_everything():
    # load corpus from parquet
    df, corpus = load_corpus_parquet("data/processed/products.parquet")

    # load BM25
    bm25, _ = load_bm25("data/processed/index")

    # load FAISS artifacts separately
    index, doc_ids, config = load_semantic_artifacts("artifacts")
    model = SentenceTransformer(config["model_name"])

    return corpus, bm25, index, doc_ids, model


corpus, bm25, faiss_index, doc_ids, model = load_everything()

st.sidebar.header("Search Settings")
method = st.sidebar.radio("Retrieval Method", ["BM25", "Semantic", "Both"])
top_k = st.sidebar.slider("Results to show", 1, 10, 5)

query = st.text_input(
    "Enter your search query", placeholder="e.g. moisturizer for dry skin"
)


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

                price_val = r.get("price")
                if price_val is None or (
                    isinstance(price_val, float) and math.isnan(price_val)
                ):
                    price_display = "N/A"
                else:
                    price_display = f"${price_val}"

                st.metric("Price", price_display)
                st.metric("Score", f"{r['score']:.4f}")
            st.divider()


if query:
    with st.spinner("Searching..."):
        if method == "Both":
            col_bm25, col_sem = st.columns(2)

            with col_bm25:
                results_bm25 = bm25_search(query, bm25, corpus, top_k=top_k)
                show_results(results_bm25, "BM25 Results")

            with col_sem:
                results_sem = semantic_search(
                    query, model, faiss_index, doc_ids, corpus, top_k=top_k
                )
                show_results(results_sem, "Semantic Results")

        else:
            if method == "BM25":
                results = bm25_search(query, bm25, corpus, top_k=top_k)
                show_results(results, "BM25 Results")
            elif method == "Semantic":
                results = semantic_search(
                    query, model, faiss_index, doc_ids, corpus, top_k=top_k
                )
                show_results(results, "Semantic Results")
else:
    st.info("Type a query above to get started.")
