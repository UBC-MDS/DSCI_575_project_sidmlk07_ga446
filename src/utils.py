import gzip
import json
import re
import pickle
import pandas as pd
from pathlib import Path

#from lecture notes
def simple_tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return text.split()


def load_jsonl_gz(filepath: str, max_records: int = None) -> list[dict]:
    """Load records from a .jsonl.gz file."""
    records = []
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_records and i >= max_records:
                break
            records.append(json.loads(line.strip()))
    return records


def build_corpus(reviews: list[dict], metadata: list[dict]) -> list[dict]:
    """
    Merge reviews and metadata into one list of documents.
    Each entry is one review, enriched with product metadata fields.

    Fields used:
      - reviews:  text, rating, asin
      - metadata: title, description, features
    
    We combine title + description + features + review text into
    a single 'combined_text' string used for indexing.
    """
    # Build a quick asin -> metadata lookup
    meta_lookup = {}
    for m in metadata:
        asin = m.get("parent_asin", "") 
        if asin:
            meta_lookup[asin] = m

    corpus = []
    for review in reviews:
        asin = review.get("parent_asin", "")
        meta = meta_lookup.get(asin, {})

        title = meta.get("title", "")

        description = meta.get("description", "")
        if isinstance(description, list):
            description = " ".join(description)

        features = meta.get("features", "")
        if isinstance(features, list):
            features = " ".join(features)

        review_text = review.get("text", "")
        rating = review.get("rating", None)
        price = meta.get("price", None)

        combined_text = f"{title} {description} {features} {review_text}"

        corpus.append({
            "asin": asin,
            "title": title,
            "review_text": review_text,
            "rating": rating,
            "price": price,
            "combined_text": combined_text,
        })

    return corpus


def save_pickle(obj, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f"Saved to {path}")


def load_pickle(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)