import sys
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import simple_tokenize, save_pickle, load_pickle


def build_bm25_index(corpus: list[dict]) -> tuple[BM25Okapi, list[list[str]]]:
    """
    Tokenize the corpus and fit a BM25 index.
    Tokenizer is the same simple_tokenize from lecture notes.
    """
    print("Tokenizing corpus...")
    tokenized_corpus = [simple_tokenize(doc["combined_text"]) for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    print(f"BM25 index ready: {len(tokenized_corpus)} documents.")
    return bm25, tokenized_corpus


def bm25_search(
    query: str, bm25: BM25Okapi, corpus: list[dict], top_k: int = 5
) -> list[dict]:
    """
    BM25 keyword search. Query is tokenized the same way as the corpus.
    Returns top_k results sorted by score descending.
    """
    tokenized_query = simple_tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    # from lecture
    ranked_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for rank, idx in enumerate(ranked_idx, start=1):
        if idx >= len(corpus):
            continue
        doc = corpus[idx].copy()
        doc["score"] = float(scores[idx])
        doc["rank"] = rank
        results.append(doc)

    return results


def save_bm25(bm25: BM25Okapi, tokenized_corpus: list[list[str]], path_prefix: str):
    save_pickle(bm25, f"{path_prefix}_bm25.pkl")
    save_pickle(tokenized_corpus, f"{path_prefix}_tokenized.pkl")


def load_bm25(path_prefix: str) -> tuple[BM25Okapi, list[list[str]]]:
    bm25 = load_pickle(f"{path_prefix}_bm25.pkl")
    tokenized_corpus = load_pickle(f"{path_prefix}_tokenized.pkl")
    return bm25, tokenized_corpus


if __name__ == "__main__":
    from utils import load_corpus_parquet

    root = Path(__file__).parent.parent

    _, corpus = load_corpus_parquet(root / "data/processed/products.parquet")
    print(f"Loaded corpus: {len(corpus)} docs")

    bm25, tokenized = build_bm25_index(corpus)
    save_bm25(bm25, tokenized, root / "data/processed/index")
    save_pickle(corpus, root / "data/processed/corpus.pkl")
    print("Corpus saved!")

    query = "moisturizer for dry skin"
    print(f"\nQUERY: {query}\n")
    for r in bm25_search(query, bm25, corpus, top_k=5):
        print(f"{r['rank']}. ({r['score']:.3f}) {r['title'][:70]}")
