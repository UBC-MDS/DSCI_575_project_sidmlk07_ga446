import sys
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  # same as lecture notes

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import save_pickle, load_pickle

MODEL_NAME = "all-MiniLM-L6-v2"  # same model as lecture notes


def build_semantic_index(corpus: list[dict], model_name: str = MODEL_NAME):
    """
    Encode all documents with sentence-transformers.
    Uses all-MiniLM-L6-v2, same model shown in lecture.
    Returns the model and the embeddings matrix.
    """
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [doc["combined_text"] for doc in corpus]
    print(f"Encoding {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Embeddings shape: {embeddings.shape}")
    return model, embeddings


def semantic_search(
    query: str,
    model: SentenceTransformer,
    embeddings: np.ndarray,
    corpus: list[dict],
    top_k: int = 5
) -> list[dict]:
    """
    Semantic search using cosine similarity between query and doc embeddings.

    Adapted directly from lecture notes:
        query_embedding = model.encode([query])
        scores = cosine_similarity(query_embedding, product_embeddings)[0]
    """
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]

    # same sorting pattern as lecture
    ranked_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for rank, idx in enumerate(ranked_idx, start=1):
        doc = corpus[idx].copy()
        doc["score"] = float(scores[idx])
        doc["rank"] = rank
        results.append(doc)

    return results


def save_semantic_artifacts(model, embeddings: np.ndarray, path_prefix: str):
    save_pickle(embeddings, f"{path_prefix}_embeddings.pkl")
    print(f"Embeddings saved to {path_prefix}_embeddings.pkl")


def load_embeddings(path_prefix: str) -> np.ndarray:
    return load_pickle(f"{path_prefix}_embeddings.pkl")


if __name__ == "__main__":
    from utils import load_jsonl_gz, build_corpus

    root = Path(__file__).parent.parent

    reviews = load_jsonl_gz(root / "data/raw/All_Beauty.jsonl.gz", max_records=500)
    metadata = load_jsonl_gz(root / "data/raw/meta_All_Beauty.jsonl.gz")  # load ALL metadata
    corpus = build_corpus(reviews, metadata)

    # sanity check
    titles_found = sum(1 for doc in corpus if doc["title"])
    print(f"Corpus: {len(corpus)} docs, {titles_found} with titles")

    model, embeddings = build_semantic_index(corpus)
    save_semantic_artifacts(model, embeddings, root / "data/processed/index")

    query = "moisturizer for dry skin"
    print(f"\nQUERY: {query}\n")
    for r in semantic_search(query, model, embeddings, corpus, top_k=5):
        print(f"{r['rank']}. ({r['score']:.3f}) {r['title'][:70]}")