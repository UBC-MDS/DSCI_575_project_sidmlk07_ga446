import gzip
import json
import re
import pickle
import pandas as pd
from pathlib import Path
import nltk
from nltk.corpus import stopwords


nltk.download("stopwords", quiet=True)
ENGLISH_STOPWORDS = set(stopwords.words("english"))


# from lecture notes
def simple_tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    words = text.split()
    return [word for word in words if word not in ENGLISH_STOPWORDS]


def load_jsonl_gz(filepath, max_records: int = None) -> list[dict]:
    """
    Incrementally load records from a .jsonl.gz file line by line.
    Avoids loading everything into memory at once (pd.read_json crashes on large files).
    Optionally cap at max_records for EDA/testing.
    """
    records = []
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_records and i >= max_records:
                break
            records.append(json.loads(line.strip()))
    return records


def jsonl_gz_to_parquet(filepath, output_path: str, max_records: int = None):
    """
    Convert a .jsonl.gz file to parquet incrementally in chunks.
    Much faster for repeated loading than re-reading the raw gz file.

    Args:
        filepath: path to .jsonl.gz file
        output_path: where to save the .parquet file
        max_records: cap records (None = full dataset)
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    chunk_size = 10_000
    chunks = []
    total = 0

    print(f"Converting {filepath} to parquet...")
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        batch = []
        for i, line in enumerate(f):
            if max_records and total >= max_records:
                break
            batch.append(json.loads(line.strip()))
            total += 1

            if len(batch) >= chunk_size:
                chunks.append(pd.DataFrame(batch))
                batch = []
                print(f"  processed {total} records...", end="\r")

        if batch:
            chunks.append(pd.DataFrame(batch))

    df = pd.concat(chunks, ignore_index=True)
    df.to_parquet(output_path, index=False)
    print(f"Saved {len(df)} records to {output_path}")
    return df


def load_parquet(path: str) -> pd.DataFrame:
    """Load a parquet file into a dataframe."""
    return pd.read_parquet(path)


def build_corpus(reviews: list[dict], metadata: list[dict]) -> list[dict]:
    """
    Merge reviews and metadata into one list of documents.
    Each entry is one review enriched with product metadata.

    Fields used:
      - reviews:  text, rating, parent_asin
      - metadata: title, description, features

    Combined into a single 'combined_text' string for indexing.
    """
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

        corpus.append(
            {
                "asin": asin,
                "title": title,
                "review_text": review_text,
                "rating": rating,
                "price": price,
                "combined_text": combined_text,
            }
        )

    return corpus


def build_corpus_from_parquet(
    reviews_df: pd.DataFrame, meta_df: pd.DataFrame
) -> list[dict]:
    """
    Same as build_corpus but takes dataframes instead of lists.
    Use this when loading from parquet files.
    """
    meta_lookup = {}
    for _, m in meta_df.iterrows():
        asin = m.get("parent_asin", "")
        if asin:
            meta_lookup[asin] = m.to_dict()

    corpus = []
    for _, review in reviews_df.iterrows():
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

        corpus.append(
            {
                "asin": asin,
                "title": title,
                "review_text": review_text,
                "rating": rating,
                "price": price,
                "combined_text": combined_text,
            }
        )

    return corpus


def save_corpus_parquet(corpus: list[dict], path: str):
    """Save corpus as parquet, one row per document, all fields preserved."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(corpus)
    df.to_parquet(path, index=False)
    print(f"Corpus saved to {path} ({len(df)} rows)")


def load_corpus_parquet(path: str) -> tuple[pd.DataFrame, list[dict]]:
    """Load corpus from parquet, return both dataframe and list of dicts."""
    df = pd.read_parquet(path)
    corpus = df.to_dict(orient="records")
    return df, corpus


def save_pickle(obj, path):
    Path(str(path)).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f"Saved to {path}")


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)
