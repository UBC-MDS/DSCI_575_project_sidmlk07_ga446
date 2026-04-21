# Final Discussion

## Step 1: Improve Your Workflow

### Dataset Scaling

- Number of products used
- Changes to sampling strategy (if any)

### LLM Experiment

- Models compared (name, family, size)
- Results and discussions
  - Prompt used (copy it here)
  - Results
- Which model you chose and why

## Step 2: Additional Feature (state which option you chose)

### What You Implemented

- Description of the feature
- Key results or examples
  
## Improved Documentation and Code Quality

### Documentation Update

We updated the `README.md` and included:

- **Usage Examples & Expected Output:** Created a dedicated section providing specific test queries (Easy, Medium, Complex) so users can test the differences between the BM25, Semantic, and AI Assistant modes.

### Code Quality Changes

We updated the codebase and made improvements to ensure it is robust, readable, and platform agnostic:

- **Docstrings:** Added descriptive docstrings to all functions across the various Python files in the `src` directory.
- **No Hardcoded Paths:** We checked all the Python files to ensure that none of them are using any hardcoded paths.

## Cloud Deployment Plan

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
