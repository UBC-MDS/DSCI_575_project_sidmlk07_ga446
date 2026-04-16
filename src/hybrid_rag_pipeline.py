import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from src.utils import load_corpus_parquet
from src.semantic import semantic_search, load_semantic_artifacts
from src.bm25 import bm25_search, load_bm25
from sentence_transformers import SentenceTransformer

llm = ChatOllama(model="llama3.2", temperature=0)
root = Path(__file__).parent.parent

_, corpus = load_corpus_parquet(root / "data/processed/products.parquet")
faiss_index, doc_ids, config = load_semantic_artifacts(root / "artifacts")
st_model = SentenceTransformer(config["model_name"])

bm25_index, _ = load_bm25(str(root / "data/processed/index"))


def get_rrf_score(item_dictionary):
    """Helper function to sort the dictionary."""
    return item_dictionary["rrf_score"]


def hybrid_retrieve_docs(query: str, top_k=5) -> list[dict]:
    """Combines BM25 and Semantic search using Reciprocal Rank Fusion (RRF)."""
    sem_results = semantic_search(
        query, st_model, faiss_index, doc_ids, corpus, top_k=15
    )
    bm25_results = bm25_search(query, bm25_index, corpus, top_k=15)

    rrf_scores = {}

    # Process Semantic Results
    for rank, doc in enumerate(sem_results, 1):
        doc_id = doc.get("parent_asin") or doc.get("asin")
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = {"rrf_score": 0.0, "doc_data": doc}
        rrf_scores[doc_id]["rrf_score"] += 1.0 / (60 + rank)

    # Process BM25 Results
    for rank, doc in enumerate(bm25_results, 1):
        doc_id = doc.get("parent_asin") or doc.get("asin")
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = {"rrf_score": 0.0, "doc_data": doc}
        rrf_scores[doc_id]["rrf_score"] += 1.0 / (60 + rank)

    sorted_fused_docs = sorted(rrf_scores.values(), key=get_rrf_score, reverse=True)

    final_docs = []
    for item in sorted_fused_docs[:top_k]:
        final_docs.append(item["doc_data"])

    return final_docs


def build_context(docs: list[dict]) -> str:
    """Converts retrieved document dictionaries into a prompt-ready context block."""
    context_str = ""
    for i, doc in enumerate(docs, 1):
        asin = doc.get("parent_asin") or doc.get("asin", "N/A")
        title = doc.get("title", "No Title")
        rating = doc.get("rating", "N/A")

        raw_price = doc.get("price")
        if raw_price is None or str(raw_price).lower() == "nan":
            price_str = "Price not listed in database"
        else:
            price_str = f"${raw_price}"

        review = doc.get("review_text", "No review")

        context_str += f"--- Product {i} ---\n"
        context_str += f"ASIN: {asin}\n"
        context_str += f"Title: {title}\n"
        context_str += f"Rating: {rating}/5 | Price: {price_str}\n"
        context_str += f"Review: {review}\n\n"

    return context_str


SYSTEM_PROMPT = """
You are a strict, factual Amazon shopping assistant.
You must answer the user's question using ONLY the provided context block (real product reviews + metadata). 

CRITICAL INSTRUCTIONS:
1. NO OUTSIDE KNOWLEDGE: Do not invent ingredients, features, or benefits. If it is not explicitly written in the context block, do not say it.
2. CITE ASIN: Always cite the product (ASIN: XXXXX) when referencing a specific product.
3. PRICE RULES: Whenever you recommend a product, you MUST state its price. If the context says "Price not listed in database", state that exact phrase. Do not guess prices.
4. NEGATIVE REVIEWS: If the context mentions a product is "not suitable", "drying", or bad for the user's specific need, explicitly exclude it or warn the user.
5. STRICT CONSTRAINTS: You must evaluate ALL adjectives and requirements in the user's query (e.g., "mineral" vs "chemical", price limits, skin types). If a product violates ANY of the user's requested constraints, you MUST NOT recommend it. If no products perfectly match all constraints, explicitly state that.

Context:
{context}

Question: 
{question}

Answer based on the Amazon datasets:
"""
prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

hybrid_retriever = RunnableLambda(hybrid_retrieve_docs)

rag_chain = (
    {"context": hybrid_retriever | build_context, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    test_query = "What is a good mineral face sunscreen with no white cast?"
    print(f"Query: {test_query}\n")
    print("Executing Hybrid Retrieval and Generating Answer...\n")

    answer = rag_chain.invoke(test_query)
    print(answer)
