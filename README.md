# Smart Amazon Product Query Assistant

A retrieval system for Amazon product reviews using BM25 and Semantic Search.

**Category used:** All Beauty

## Team
- Gaurang Ahuja (ga446)
- Sidharth Malik (sidmlk07)

## Setup

### 1. Clone the repo
```bash
git clone git@github.com:UBC-MDS/DSCI_575_project_sidmlk07_ga446.git
cd DSCI_575_project_sidmlk07_ga446
```

### 2. Create environment
```bash
conda env create -f environment.yml
conda activate dsci575
```

### 3. Download data
Download `All_Beauty.jsonl.gz` and `meta_All_Beauty.jsonl.gz` from
https://amazon-reviews-2023.github.io/ and place in `data/raw/`.

### 4. Build indexes
Run the EDA notebook first, then:
```bash
python src/bm25.py
python src/semantic.py
```

### 5. Run the app
```bash
streamlit run app/app.py
```

## Dataset
Amazon Reviews 2023 — All Beauty category.
- Reviews file: ratings, review text, timestamps
- Metadata file: product title, description, features, price

## Retrieval Methods
- **BM25** (`src/bm25.py`): keyword-based, uses `rank_bm25`
- **Semantic** (`src/semantic.py`): embedding-based, uses `sentence-transformers` + FAISS
- **Utils** (`src/utils.py`): data loading, tokenization, corpus building