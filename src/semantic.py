import sys
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import save_pickle, load_pickle

MODEL_NAME = "all-MiniLM-L6-v2"


def build_semantic_index(corpus: list[dict], model_name: str = MODEL_NAME):
    """
    Encode all documents with sentence-transformers (all-MiniLM-L6-v2)
    and build a FAISS index for fast similarity search.
    
    Uses IndexFlatIP (inner product) with L2-normalized vectors,
    which is equivalent to cosine similarity.
    """
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [doc["combined_text"] for doc in corpus]
    print(f"Encoding {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    faiss.normalize_L2(embeddings)

    #FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"FAISS index built — {index.ntotal} vectors (dim={dim})")
    return model, index, embeddings


def semantic_search(
    query: str,
    model: SentenceTransformer,
    index: faiss.Index,
    corpus: list[dict],
    top_k: int = 5
) -> list[dict]:
    """
    Semantic search using FAISS index.
    Query is encoded and L2-normalized, then searched via inner product
    (equivalent to cosine similarity after normalization).
    """
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    # FAISS
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
        doc = corpus[idx].copy()
        doc["score"] = float(score)
        doc["rank"] = rank
        results.append(doc)

    return results


def save_semantic_index(index: faiss.Index, path: str):
    """Save FAISS index using faiss.write_index as instructed in milestone."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(path))
    print(f"FAISS index saved to {path}")


def load_semantic_index(path: str) -> faiss.Index:
    """Load FAISS index using faiss.read_index."""
    return faiss.read_index(str(path))


if __name__ == "__main__":
    from utils import load_jsonl_gz, build_corpus

    root = Path(__file__).parent.parent

    reviews = load_jsonl_gz(root / "data/raw/All_Beauty.jsonl.gz", max_records=500)
    metadata = load_jsonl_gz(root / "data/raw/meta_All_Beauty.jsonl.gz")
    corpus = build_corpus(reviews, metadata)

    titles_found = sum(1 for doc in corpus if doc["title"])
    print(f"Corpus: {len(corpus)} docs, {titles_found} with titles")

    model, index, _ = build_semantic_index(corpus)

    save_semantic_index(index, root / "data/processed/faiss.index")
    save_pickle(model, root / "data/processed/model.pkl")

    query = "moisturizer for dry skin"
    print(f"\nQUERY: {query}\n")
    for r in semantic_search(query, model, index, corpus, top_k=5):
        print(f"{r['rank']}. ({r['score']:.3f}) {r['title'][:70]}")