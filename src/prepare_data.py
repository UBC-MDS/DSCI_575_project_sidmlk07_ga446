import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import (
    jsonl_gz_to_parquet,
    build_corpus_from_parquet,
    save_corpus_parquet,
    load_parquet,
)

root = Path(__file__).parent.parent

CATEGORY = "All_Beauty"
# Kept at 65000 for faster processing
# Update to `None` for capable machines
MAX_REVIEWS = 65000

reviews_parquet = root / "data/processed/reviews.parquet"
meta_parquet = root / "data/processed/metadata.parquet"

if not reviews_parquet.exists():
    jsonl_gz_to_parquet(
        root / f"data/raw/{CATEGORY}.jsonl.gz", reviews_parquet, max_records=MAX_REVIEWS
    )
else:
    print(f"Reviews parquet already exists, skipping conversion.")

if not meta_parquet.exists():
    jsonl_gz_to_parquet(root / f"data/raw/meta_{CATEGORY}.jsonl.gz", meta_parquet)
else:
    print(f"Metadata parquet already exists, skipping conversion.")

products_parquet = root / "data/processed/products.parquet"

if not products_parquet.exists():
    print("Building corpus from parquet files...")
    reviews_df = load_parquet(reviews_parquet)
    meta_df = load_parquet(meta_parquet)

    print(f"Reviews: {len(reviews_df)} rows")
    print(f"Metadata: {len(meta_df)} rows")

    corpus = build_corpus_from_parquet(reviews_df, meta_df)
    titles_found = sum(1 for doc in corpus if doc["title"])
    print(f"Corpus: {len(corpus)} docs, {titles_found} with titles")

    save_corpus_parquet(corpus, products_parquet)
else:
    print(f"Products parquet already exists, skipping.")

print("\nDone! You can now run:")
print("  python src/bm25.py")
print("  python src/semantic.py")
print("  streamlit run app/app.py")
