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
    Encode all documents with sentence-transformers and build a FAISS index.
    
    Scalability decisions:
    - Batched encoding (batch_size=256) avoids memory overflow at 100k+ docs
    - IndexIVFFlat with nlist=256 clusters for fast approximate search at scale
      (exact IndexFlatIP becomes too slow beyond ~50k vectors)
    - Falls back to IndexFlatIP for small corpora (<10k docs) where IVF overhead
      isn't worth it
    """
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [doc["combined_text"] for doc in corpus]
    n = len(texts)
    print(f"Encoding {n} documents in batches...")

    embeddings = model.encode(
        texts,
        batch_size=256,
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    if n >= 10_000:
        nlist = 256
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
        print(f"Training IVFFlat index (nlist={nlist})...")
        index.train(embeddings)
        index.add(embeddings)
        index.nprobe = 32
    else:
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
    """Save FAISS index, doc_ids mapping, and config."""
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(artifacts_dir / "faiss_index.bin"))
    print(f"FAISS index saved to {artifacts_dir / 'faiss_index.bin'}")

    doc_ids = np.arange(len(corpus))
    np.save(str(artifacts_dir / "doc_ids.npy"), doc_ids)

    config = {
        "model_name": model_name,
        "text_fields_used": ["title", "description", "features", "review_text"],
        "combined_field": "combined_text",
        "num_documents": len(corpus),
        "embedding_dim": index.d,
        "similarity": "cosine (IndexFlatIP + L2 norm)" if len(corpus) < 10_000
                      else "cosine approx (IndexIVFFlat nlist=256 nprobe=32)",
        "index_type": "IndexFlatIP" if len(corpus) < 10_000 else "IndexIVFFlat",
        "nprobe": 32 if len(corpus) >= 10_000 else None,
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
    if config.get("nprobe") and hasattr(index, "nprobe"):
        index.nprobe = config["nprobe"]
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
    2. Search FAISS for top_k nearest vectors (fetch more to account for dedup)
    3. Deduplicate by parent_asin, keep highest scoring review per product
    4. Return top_k unique products sorted by score
    """
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k * 10)

    seen_asins = set()
    results = []
    rank = 1

    for score, idx in zip(scores[0], indices[0]):
        corpus_idx = doc_ids[idx]
        doc = corpus[corpus_idx].copy()
        asin = doc.get("asin", "") or doc.get("parent_asin", "")

        if asin and asin in seen_asins:
            continue

        seen_asins.add(asin)
        doc["score"] = float(score)
        doc["rank"] = rank
        results.append(doc)
        rank += 1

        if len(results) >= top_k:
            break

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