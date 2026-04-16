import sys
import streamlit as st
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_corpus_parquet, load_pickle
from src.bm25 import bm25_search, load_bm25
from src.semantic import semantic_search, load_semantic_artifacts
from src.hybrid_rag_pipeline import rag_chain, hybrid_retrieve_docs
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


tab_rag, tab_search = st.tabs(
    ["🤖 RAG Assistant (Milestone 2)", "🔍 Search Only (Milestone 1)"]
)

with tab_rag:
    if st.button("Generate AI Answer", type="primary") and query:
        st.divider()

        st.subheader("✨ AI Shopping Assistant")
        with st.spinner("Reading reviews and generating answer..."):
            ai_response = rag_chain.invoke(query)
            st.info(ai_response)

        st.divider()

        st.subheader("Source Documents (Hybrid Search)")
        with st.spinner("Loading source details..."):
            retrieved_docs = hybrid_retrieve_docs(query)

            if not retrieved_docs:
                st.warning("No products found.")
            else:
                for i, doc in enumerate(retrieved_docs, 1):
                    asin = doc.get("parent_asin") or doc.get("asin", "N/A")
                    title = doc.get("title", "No Title")
                    rating = doc.get("rating", "N/A")

                    price_val = doc.get("price")
                    if price_val is None or (
                        isinstance(price_val, float) and math.isnan(price_val)
                    ):
                        price_display = "Price not listed"
                    else:
                        price_display = f"${price_val}"

                    raw_review = doc.get("review_text", "No review text available.")
                    trunc_review = (
                        raw_review[:250] + "..."
                        if len(raw_review) > 250
                        else raw_review
                    )

                    with st.expander(f"[{i}] {title[:80]}... | ⭐ {rating}/5"):
                        st.caption(f"**ASIN:** {asin} | **Price:** {price_display}")
                        st.markdown(f"**Review Snippet:** _{trunc_review}_")

with tab_search:
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
