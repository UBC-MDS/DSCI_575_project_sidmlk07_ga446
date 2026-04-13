import sys
import numpy as np
import faiss
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).parent.parent))

MODEL_NAME = "all-MiniLM-L6-v2"


def build_semantic_index(corpus: list[dict], model_name: str = MODEL_NAME):
    """
    Encode all documents with sentence transformers (all-MiniLM-L6-v2)
    and build a FAISS index for fast similarity search.
    Uses IndexFlatIP (inner product) with L2-normalized vectors,
    equivalent to cosine similarity.
    """
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [doc["combined_text"] for doc in corpus]
    print(f"Encoding {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"FAISS index built — {index.ntotal} vectors (dim={dim})")
    return model, index


def save_semantic_artifacts(
    index: faiss.Index,
    corpus: list[dict],
    model_name: str,
    artifacts_dir: str
):
    """
    Save FAISS index, doc_ids mapping, and config separately.
    """
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(artifacts_dir / "faiss_index.bin"))
    print(f"FAISS index saved to {artifacts_dir / 'faiss_index.bin'}")

    doc_ids = np.arange(len(corpus))
    np.save(str(artifacts_dir / "doc_ids.npy"), doc_ids)
    print(f"doc_ids saved to {artifacts_dir / 'doc_ids.npy'}")

    config = {
        "model_name": model_name,
        "text_fields_used": ["title", "description", "features", "review_text"],
        "combined_field": "combined_text",
        "num_documents": len(corpus),
        "embedding_dim": index.d,
        "similarity": "cosine (IndexFlatIP + L2 norm)"
    }
    with open(artifacts_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {artifacts_dir / 'config.json'}")


def load_semantic_artifacts(artifacts_dir: str):
    """Load FAISS index, doc_ids, and config from artifacts directory."""
    artifacts_dir = Path(artifacts_dir)
    index = faiss.read_index(str(artifacts_dir / "faiss_index.bin"))
    doc_ids = np.load(str(artifacts_dir / "doc_ids.npy"))
    with open(artifacts_dir / "config.json") as f:
        config = json.load(f)
    return index, doc_ids, config


def semantic_search(
    query: str,
    model: SentenceTransformer,
    index: faiss.Index,
    doc_ids: np.ndarray,
    corpus: list[dict],
    top_k: int = 5
) -> list[dict]:
    """
    Semantic search using FAISS index.
    1. Embed and normalize query
    2. Search FAISS for top_k nearest vectors
    3. Use doc_ids to look up original corpus rows
    4. Return results with scores
    """
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
        corpus_idx = doc_ids[idx]         
        doc = corpus[corpus_idx].copy()
        doc["score"] = float(score)
        doc["rank"] = rank
        results.append(doc)

    return results


if __name__ == "__main__":
    from utils import load_corpus_parquet

    root = Path(__file__).parent.parent

    _, corpus = load_corpus_parquet(root / "data/processed/products.parquet")
    titles_found = sum(1 for doc in corpus if doc["title"])
    print(f"Loaded corpus: {len(corpus)} docs, {titles_found} with titles")

    model, index = build_semantic_index(corpus)

    save_semantic_artifacts(index, corpus, MODEL_NAME, root / "artifacts")

    query = "moisturizer for dry skin"
    print(f"\nQUERY: {query}\n")

    index, doc_ids, config = load_semantic_artifacts(root / "artifacts")
    for r in semantic_search(query, model, index, doc_ids, corpus, top_k=5):
        print(f"{r['rank']}. ({r['score']:.3f}) {r['title'][:70]}")