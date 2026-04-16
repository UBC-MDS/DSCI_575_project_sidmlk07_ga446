import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from src.utils import load_corpus_parquet
from src.semantic import semantic_search, load_semantic_artifacts
from sentence_transformers import SentenceTransformer

llm = ChatOllama(model="llama3.2", temperature=0)

root = Path(__file__).parent.parent
_, corpus = load_corpus_parquet(root / "data/processed/products.parquet")
faiss_index, doc_ids, config = load_semantic_artifacts(root / "artifacts")
st_model = SentenceTransformer(config["model_name"])


def retrieve_docs(query: str) -> list[dict]:
    """Retrieves top-5 documents using semantic search."""
    return semantic_search(query, st_model, faiss_index, doc_ids, corpus, top_k=5)


def build_context(docs: list[dict]) -> str:
    """Converts retrieved document dictionaries into a prompt-ready context block."""
    context_str = ""
    for i, doc in enumerate(docs, 1):
        asin = doc.get("asin", "N/A")
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
5. CONSTRAINTS: Only apply constraints (like price limits or skin types) if the user explicitly asks for them in their question.

Context:
{context}

Question: 
{question}

Answer based on the Amazon datasets:
"""

prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

retriever = RunnableLambda(retrieve_docs)

rag_chain = (
    {"context": retriever | build_context, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    test_query = "What is a good moisturizer for extremely dry skin?"
    print(f"Query: {test_query}\n")
    print("Thinking...\n")

    answer = rag_chain.invoke(test_query)
    print(answer)
