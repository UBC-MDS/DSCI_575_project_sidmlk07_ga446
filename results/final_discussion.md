# Final Discussion

## Step 1: Improve Your Workflow

### 1.1 Dataset Scaling

For Milestone 1, the pipeline was capped at `MAX_REVIEWS = 5000` due to CPU encoding
constraints during development. For the final submission, we changed it to 65000.
Locally, we also tested with the **FULL** dataset, results for which are in the table below.

| Metric | Full Dataset Testing |
|---|---|
| Reviews loaded | 701,528 |
| Unique products  | 112,565 |
| Average reviews per product | ~6.2 |

The full dataset required engineering changes to avoid performance bottlenecks, these
are documented in detail under Step 2 (Option 3: Scale to 100k+).

---

### 1.2 LLM Comparison

#### Models Compared

| Model | Family | Parameters | Provider |
|---|---|---|---|
| `llama3.2` | Meta Llama 3 | 3B | Meta |
| `phi4-mini` | Phi-4 | 3.8B | Microsoft |

Both models were run locally via Ollama on a MacBook Pro M4 (16GB unified memory).
Both received identical retrieved context (top-5 hybrid RRF documents) and the same
system prompt for every query.

#### Prompt Used

```
You are a strict, factual Amazon shopping assistant.
You must answer the user's question using ONLY the provided context block
(real product reviews + metadata).

CRITICAL INSTRUCTIONS:
1. NO OUTSIDE KNOWLEDGE: Do not invent ingredients, features, or benefits.
   If it is not explicitly written in the context block, do not say it.
2. CITE ASIN: Always cite the product (ASIN: XXXXX) when referencing a product.
3. PRICE RULES: Whenever you recommend a product, you MUST state its price.
   If the context says "Price not listed in database", state that exact phrase.
   Do not guess prices.
4. NEGATIVE REVIEWS: If the context mentions a product is "not suitable",
   "drying", or bad for the user's specific need, explicitly exclude it or
   warn the user.
5. STRICT CONSTRAINTS: You must evaluate ALL adjectives and requirements in
   the user's query. If a product violates ANY of the user's requested
   constraints, you MUST NOT recommend it.

Context:
{context}

Question:
{question}

Answer based on the Amazon dataset:
```

#### Queries Tested

1. `best moisturizer for dry sensitive skin`
2. `gentle face wash that does not strip skin`
3. `vitamin C serum for brightening dark spots`
4. `affordable shampoo for damaged hair`
5. `what is a good daily sunscreen for dark skin tones that leaves no white cast`

#### Results

| Query | llama3.2 | phi4-mini |
|---|---|---|
| Moisturizer for dry sensitive skin | Recommended 2 relevant products, correctly excluded the poor-reviewed DayTime Moisturizer, cited ASINs and noted missing prices | Focused single recommendation with clear reasoning, slightly less comprehensive |
| Gentle face wash | Single focused recommendation with direct quote from review as evidence | Recommended 2 products with brief reasoning, slightly more verbose but accurate |
| Vitamin C serum | Best match with detailed review evidence cited | Listed 3 products, slightly less focused but still grounded in context |
| Affordable shampoo for damaged hair | 3 relevant recommendations, correctly noted all prices were missing from database | **Critical failure**: after a brief opening answer, entered an infinite loop generating dozens of fabricated follow-up questions and invented a product ("Kérastop Volume 2") that does not exist anywhere in the dataset |
| Sunscreen for dark skin tones | Correctly identified Country and Stream Honey UV gel as best match, cited reviewer who explicitly mentioned dark skin and no white cast | **Critical failure**: produced incoherent self-referential output, repeatedly regenerating its own "fact-checker" prompt instructions and losing the original query entirely |

#### Key Observations

**1. Instruction following**

`llama3.2` consistently respected all system prompt constraints across all
queries. `phi4-mini` followed instructions adequately on simpler queries (1–3) but
catastrophically failed on queries 4 and 5, generating infinite loops of fabricated
content well beyond the context window.

**2. Hallucination**

`llama3.2` produced zero hallucinations; every cited product, price, and claim was
grounded in the provided context block. `phi4-mini` invented an entire product
("Kérastop Volume 2") that does not exist in the dataset, a direct violation of the
NO OUTSIDE KNOWLEDGE constraint.

**3. Context boundary awareness**

`llama3.2` stayed strictly within the provided context. `phi4-mini` lost the context
boundary on complex queries, effectively beginning to generate its own prompts and
re-running itself in a loop.

**4. Response conciseness**

`llama3.2` responses were concise, structured, and directly actionable.
`phi4-mini` responses, when not failing, were slightly more verbose but reasonable.

#### Conclusion

**`llama3.2` remains the default model for our production pipeline.** `phi4-mini`'s
failures on queries 4 and 5 are likely attributable to its smaller instruction-tuning
dataset and known sensitivity to strict multi-constraint prompts. The phi architecture
excels at reasoning and math tasks but is less reliable as a constrained RAG shopping
assistant. This comparison confirms that model selection for RAG systems should
prioritize instruction-following reliability over raw parameter count.

---

## Step 2: Additional Feature: Scale to 100k+ Products (Option 3)

### Overview

This milestone focused on engineering scalability to handle the full All_Beauty
dataset of **701,528 review documents across 112,565 unique products**. These targeted
changes were made to the pipeline to prevent performance breakdowns at this scale.

---

### What Broke at Small Scale (and Why)

**1. `iterrows()` in corpus construction**

The original `build_corpus_from_parquet()` used `pandas.DataFrame.iterrows()` to loop
over reviews and look up metadata via a Python dictionary. While readable, `iterrows()`
constructs a full Python object for every row, bypassing pandas' vectorized C
internals. At 5,000 rows this was acceptable, but at 700k+ rows this becomes a
bottleneck of several minutes just for the merge step.

**2. `IndexFlatIP` for semantic search**

The FAISS index used `IndexFlatIP`, which performs exact exhaustive
search; every query vector is compared against every document vector. At 5,000
documents this is fast (<10ms per query). At 700k+ documents, query latency grows
linearly and becomes noticeably slow in a live app setting.

**3. Encoding all documents in one call**

The original `model.encode(texts)` call passed the entire corpus at once. At 700k+
documents this risks exhausting available RAM since all embeddings must be held in
memory simultaneously before being added to the index.

**4. Duplicate results in semantic search**

At 5,000 documents the dataset was small enough that popular products had only a few
reviews each, so duplicates rarely surfaced in the top-5. At 700k documents, a popular
product with hundreds of reviews would flood the top-k results with near-identical
embeddings. A deduplication step was needed.

---

### Engineering Changes Made

**1. Vectorized corpus construction**

Replaced `iterrows()` with a pandas `merge()` operation, joining reviews to metadata
on `parent_asin` in a single vectorized pass. List-type fields (`description`,
`features`) are flattened to strings using `apply()` before the merge. This reduces
corpus construction from an O(n) Python loop to a single optimized join.

**2. Batched semantic encoding**

Updated `build_semantic_index()` to encode documents in batches of 256:

```python
embeddings = model.encode(texts, batch_size=256, show_progress_bar=True)
```

This keeps memory usage bounded; only 256 document embeddings are processed at a
time, making it feasible to encode 700k+ documents on CPU without out of memory
errors.

**3. IVFFlat index for approximate nearest neighbour search**

For corpora of 10,000+ documents, we switch from `IndexFlatIP` (exact search) to
`IndexIVFFlat` (approximate search):

```python
nlist = 256   # number of Voronoi cells / clusters
nprobe = 32   # number of clusters to search at query time
```

`IndexIVFFlat` clusters all document vectors into `nlist=256` buckets using a flat
quantizer. At query time, only the `nprobe=32` nearest clusters are searched rather
than the full index, roughly an 8x reduction in comparisons per query. Searching
32 of 256 clusters (12.5% of the index) in practice recovers >95% of the exact top-k
results for dense retrieval tasks. The `nprobe` value is saved in
`artifacts/config.json` and restored automatically on load.

**4. Deduplication by `parent_asin` in semantic search**

Updated `semantic_search()` to fetch `top_k * 10` candidates from FAISS, then walk
through them skipping any `parent_asin` already seen. This ensures the top-5 results
represent 5 different products rather than 5 reviews of the same popular product:

```python
# Fetch top_k * 10 to have enough candidates after dedup
scores, indices = index.search(query_embedding, top_k * 10)

seen_asins = set()
for score, idx in zip(scores[0], indices[0]):
    asin = corpus[doc_ids[idx]].get("asin", "")
    if asin in seen_asins:
        continue
    seen_asins.add(asin)
    # append to results...
```

---

### Results

| Metric | Value |
|---|---|
| Total review documents indexed | 701,528 |
| Unique products | 112,565 |
| Average reviews per product | ~6.2 |
| Semantic encoding time (CPU, M4) | ~28 min (encoding) + ~2 min (IVF training) = ~30 min total |
| BM25 index build time | < 1 minute |
| FAISS index type | IndexIVFFlat (nlist=256, nprobe=32) |
| Embedding dimension | 384 |
| Machine | MacBook Pro M4, 16GB unified memory |

---

### Design Decisions Summary

| Decision | Rationale |
|---|---|
| `pandas.merge()` over `iterrows()` | Vectorized C-level operation; orders of magnitude faster for large DataFrames |
| `batch_size=256` for encoding | Bounds peak memory usage; safe for CPU without out-of-memory errors at 700k docs |
| `IndexIVFFlat` over `IndexFlatIP` | Sub-linear query time at 700k scale; >95% recall recovery with nprobe=32 |
| `nlist=256` | Standard rule of thumb: ~√n clusters for n~100k documents |
| `nprobe=32` | 12.5% of clusters searched — good speed/accuracy balance for dense retrieval |
| Threshold at 10k docs | Below 10k, exact search is fast enough; IVF training overhead not worth it |
| Dedup by `parent_asin` | Prevents popular products from flooding top-k with near-identical review embeddings |

### Known Limitation

Each document in the corpus corresponds to one review, not one product. Even with
deduplication at query time, the underlying index contains 701,528 vectors for 112,565
products. A future improvement would be to aggregate all reviews per product into a
single document before indexing, which would reduce the index size by ~6x and improve
both build time and result diversity.

---

## Step 3: Documentation and Code Quality

### Documentation Update

We updated the `README.md` and included:

- **Usage Examples & Expected Output:** Created a dedicated section providing specific
  test queries (Easy, Medium, Complex) so users can test the differences between the
  BM25, Semantic, and AI Assistant modes.
- **Updated Dataset Description:** Reflects the full All_Beauty corpus (701,528
  reviews, 112,565 unique products) and removes the previous note about the 5,000
  review cap from Milestone 1.
- **Index Rebuild Instructions:** Updated to note the ~30 minute encoding time for the
  full dataset so users know what to expect.

### Code Quality Changes

We updated the codebase to ensure it is robust, readable, and platform agnostic:

- **Docstrings:** Added descriptive docstrings to all functions across the Python files
  in the `src` directory.
- **No Hardcoded Paths:** Verified all Python files use `Path(__file__).parent.parent`
  anchored paths instead of relative strings, ensuring scripts run correctly regardless
  of working directory. This was particularly important for `app/app.py` which broke
  when Streamlit was launched from outside the project root.
- **`nprobe` Persistence:** `save_semantic_artifacts()` now saves `nprobe` to
  `artifacts/config.json` and `load_semantic_artifacts()` restores it on load,
  ensuring consistent query-time performance without manual configuration after scaling
  to IVFFlat.
- **Semantic Search Deduplication:** Updated `semantic_search()` to fetch `top_k * 10`
  candidates and deduplicate by `parent_asin` before returning results. This was
  necessary at 700k scale where popular products with many reviews would otherwise
  flood the top-k with near-identical embeddings.

## Step 4: Cloud Deployment Plan

To transition our Amazon Product Recommendation tool from a local development environment to a scalable production environment, we will utilize AWS, specifically leveraging the big data and cloud computing tools covered in our curriculum.

### 1. Data Storage

We will move away from local disk storage and utilize cloud object storage, optimizing our file formats for efficient querying.

- **a. Raw Data:** The raw Amazon `.jsonl.gz` review files will be dumped directly into an **Amazon S3** bucket. S3 acts as our scalable data lake.
- **b. Processed Data:** The cleaned data will be saved back to S3 in **Parquet** format. By storing the data as Parquet, we utilize columnar storage, which drastically reduces I/O bottlenecks. In memory, this data will be backed by **Apache Arrow** to ensure zero copy reads and high speed analytical processing.
- **c. Vector & BM25 Indices:** For a baseline deployment, the `.faiss` and `.pkl` artifacts can be stored in S3. When our application boots up, it will download these indices from S3 into the application's RAM for fast, in memory retrieval.

### 2. Compute

Our compute strategy relies on explicitly provisioned virtual machines and highly optimized analytical engines.

- **a. Where will the app run?** The Streamlit frontend will be hosted on an **Amazon EC2 instance**. We will provision an appropriately sized EC2 instance, SSH into it, set up our Python environment, and launch the Streamlit server, binding it to the public IP address.
- **b. Handling Multiple Users (Concurrency):** Instead of loading massive Pandas dataframes into our EC2's limited memory, we will use **DuckDB**. DuckDB can execute ultra fast analytical SQL queries directly against the Parquet files sitting in S3. This allows us to handle concurrent user filtering (e.g., finding products under $30) without crashing the EC2 instance due to out-of-memory (OOM) errors.
- **c. Handling LLM inference** Running a 3B parameter Llama model on a standard CPU EC2 instance would be really slow and cause timeouts. To solve this, we will separate the web server from the AI compute using one of two methods:
  - **Option 1 (GPU EC2):** We provision a specialized, GPU-backed EC2 instance (like the `g4dn` family) dedicated entirely to running the LLM. Our main Streamlit EC2 instance will send the queries and context directly to this GPU machine to process.
  - **Option 2 (Managed Cloud API):** To avoid the high costs and maintenance of running our own GPUs, we can use a managed cloud API. We would simply store a provider key (e.g., `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`) in a `.env` file on our Streamlit server and send our RAG queries directly to their hosted LLMs.

### 3. Streaming/Updates

To handle the incorporation of thousands of new daily Amazon reviews, we will make use of distributed computing.

- **a. Incorporating New Products:** When new batches of raw reviews arrive in our S3 bucket, processing them on a single machine using Pandas would eventually fail. Instead, we will spin up an **Amazon EMR** cluster.
- **b. Keeping the pipeline up to date:** We will write an **Apache Spark** job (PySpark) to run on the EMR cluster. Spark will distribute the workload across the underlying **Hadoop** ecosystem, allowing us to clean the new text, generate new embeddings in parallel across multiple worker nodes, and write the new records to S3 as partitioned Parquet files efficiently. Once the EMR job finishes, our EC2 application simply reloads the updated indices.
