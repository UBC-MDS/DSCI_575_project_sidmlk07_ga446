# Smart Amazon Product Query Assistant

## Overview
A retrieval system for Amazon product reviews that allows users to search for products using both keyword based (BM25) and semantic (vector embedding) search methods.

**Dataset Category:** All Beauty (Amazon Reviews 2023)

## Team
- Gaurang Ahuja (ga446)
- Sidharth Malik (sidmlk07)

## Setup

### 1. Clone the repo
```bash
git clone git@github.com:UBC-MDS/DSCI_575_project_sidmlk07_ga446.git
cd DSCI_575_project_sidmlk07_ga446
```

### 2. Create and activate the environment
This project uses Conda for environment management.
```bash
conda env create -f environment.yml
conda activate dsci575
```

### 3. Configure environment variables
Create a `.env` file in the root directory of the project. Add any necessary environment variables or API keys required for the app to run:
```bash
cp .env.example .env
```

### 4. Download data
Download the `All_Beauty.jsonl.gz` and `meta_All_Beauty.jsonl.gz` files from
[Amazon Reviews 2023 Dataset](https://amazon-reviews-2023.github.io/) and place them in `data/raw/`.

### 5. Build indexes
Run the exploratory data analysis (EDA) notebook first (`milestone1_exploration.ipynb`) to understand the data. Then run the following in sequence:
```bash
python src/prepare_data.py
python src/bm25.py
python src/semantic.py
```

### 6. Run the app
Run the Streamlit app locally:
```bash
streamlit run app/app.py
```

## Dataset & Data Processing

**Source:** Amazon Reviews 2023 (All Beauty category).
- **Reviews file:** Contains user ratings, review text, timestamps, and product IDs.
- **Metadata file:** Contains product titles, descriptions, features, and pricing.

**Preprocessing Steps (`src/utils.py`):**
To prepare the data for retrieval, we execute the following pipeline:
1. **Field Merging:** We join the reviews and metadata using `parent_asin` and combine the `title`, `description`, `features`, and `review_text` into a single `combined_text` field for each document. Missing fields are safely imputed with empty strings.
2. **Text Normalization:** The combined text is converted to lowercase to ensure case insensitive matching.
3. **Punctuation Removal:** Special characters and punctuation are stripped using regular expressions.
4. **Stopword Removal:** Common English stopwords are filtered out using the NLTK library to reduce noise for the BM25 index and prevent common words (like "for" or "the") from skewing results.


## Retrieval Methods
Our application allows users to compare two distinct retrieval systems i.e. BM25 and semantic search:

### 1. BM25 (Keyword Search)
- **File:** `src/bm25.py`
- **Workflow:** Uses the `rank_bm25` package (`BM25Okapi`). The preprocessed `combined_text` corpus is tokenized and indexed. When a user submits a query, it undergoes the exact same preprocessing pipeline (lowercasing, punctuation/stopword removal) before being scored against the index using exact term matching, term frequency, and inverse document frequency. The index and tokenized corpus are serialized and saved as `.pkl` files for fast loading.

### 2. Semantic Search (Dense Vector Retrieval)
- **File:** `src/semantic.py`
- **Workflow:** Uses `sentence-transformers` (specifically `all-MiniLM-L6-v2`) to convert the `combined_text` of each document into dense vector embeddings. The embeddings are L2-normalized and indexed using **FAISS** (`IndexFlatIP`) for inner-product similarity search (mathematically equivalent to cosine similarity after normalization). User queries are embedded on the fly, normalized, and compared against the FAISS index to find the nearest semantic neighbors.