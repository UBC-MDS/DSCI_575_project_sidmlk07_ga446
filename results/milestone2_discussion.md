# Milestone 2 - RAG Pipeline: Semantic and Hybrid Retrieval

## 1. Model Choice & Rationale

For the LLM generator, we selected `meta-llama/Llama-3.2-3B-Instruct` to be used locally via Ollama. Since both of us have an Apple M4 chip with unified memory, this allows us to use this 3 billion parameter model to execute with high speed and low latency. We specifically opted for the "Instruct" variant, as our LangChain RAG pipeline requires the model to strictly adhere to formatting constraints and base its answers purely on retrieved context rather than its internal memory. We utilize the `langchain_ollama` wrapper to integrate it seamlessly into our pipeline.

---

## 2. Prompt Template Design & Experimentation

To optimize our LLM Generator's output and eliminate hallucinations, we experimented with three distinct system prompts, discovering and patching flaws iteratively:

**Variant 1: Basic Conversational Prompt**

- *Prompt:* "You are a helpful Amazon shopping assistant. Answer the question using ONLY the following context. Always cite the product ASIN."
- *Result:* The model successfully cited ASINs but suffered from **Metadata Hallucination**. Because some products in the Amazon dataset are missing price data (stored as `NaN`), the prompt passed missing values to the model. In an attempt to be helpful, the LLM hallucinated a price, stating a product was "priced around $25-$30" based entirely on its pre-trained knowledge of what lotions typically cost.

**Variant 2: Strict Constraints with Examples**

- *Prompt:* We added rules telling it not to guess prices, and included an example constraint: *(e.g., price limits like "under $30")*.
- *Result:* The model stopped guessing prices, but fell into two new traps. First, it read the "$30" example in the system prompt and hallucinated that the user had a strict budget, even when the user didn't mention price. Second, it hallucinated ingredients (like "aloe vera" and "chamomile") that were not in the review context, drawing on its memory to make the product sound better.

**Variant 3: The Strict Factual Prompt (Semantic Baseline)**

- *Prompt:* We removed the misleading examples and added a strict `NO OUTSIDE KNOWLEDGE` clause. We explicitly commanded it to state "Price not listed" if the metadata was missing, and added a rule to exclude products if reviews mentioned negative side effects (e.g., "drying").
- *Result:* This prompt led to much better output. the LLM successfully identified negative constraints (warning the user that a product was "drying" for dry skin), it handled missing prices without guessing, and it strictly anchored its ingredient claims to the provided context block.

**Variant 4: The Hybrid Refinement (Final Production Prompt)**

- *Prompt:* During our initial Hybrid RAG testing, the model successfully found a product that matched "no white cast," but it failed the user's "mineral" constraint (recommending a chemical sunscreen instead). To fix this prioritization flaw, we updated Rule #5 to explicitly command: *"STRICT CONSTRAINTS: You must evaluate ALL adjectives in the user's query... If a product violates ANY of the requested constraints, you MUST NOT recommend it."*
- *Result:* The LLM successfully corrected its behavior. It learned to strictly enforce all adjectives (like "mineral" vs. "chemical") as non-negotiable filters, rather than ignoring one constraint just to satisfy another. If a perfect match could not be found, it honestly admitted it, resulting in a perfectly constrained final output.

## Step 3: RAG Evaluation

### 3.1 Manual / Qualitative Evaluation for Hybrid RAG Workflow

**Evaluation Table**
*Note: Evaluated using the Hybrid RAG pipeline (BM25 + Semantic via Reciprocal Rank Fusion) with Llama 3.2.*

| Query | Accuracy | Completeness | Fluency | Brief Notes on Output |
| :--- | :--- | :--- | :--- | :--- |
| 1. `hydrating face moisturizer` (Easy) | Yes | Yes | Yes | *Successfully returned and summarized basic moisturizers.* |
| 2. `product to keep my hair from getting frizzy in the rain` (Medium) | Yes | Yes | Yes | *Semantic search correctly mapped "rain" to humidity/anti-frizz products.* |
| 3. `good gift for someone who loves doing their makeup` (Medium) | Yes | Yes | Yes | *Handled the conceptual nature of "gifting" well.* |
| 4. `what is a good daily sunscreen for dark skin tones that leaves no white cast` (Complex) | Yes | Yes | Yes | *Strictly adhered to the 'no white cast' constraint from our prompt engineering.* |
| 5. `what is the best fragrance-free moisturizer for sensitive skin under $30` (Complex) | Yes | Yes | Yes | *Found fragrance-free options, as the price was not listed, model mentioned it specifically which is good* |

### 3.2 Evaluation Summary

**a. Key Observations and Overall Performance:**

The Hybrid RAG workflow performed exceptionally well at understanding both exact keywords and broad semantic concepts, successfully grounding its answers in the provided context. Llama 3.2 demonstrated high fluency, synthesizing multiple product reviews into readable, natural recommendations. Thanks to our rigorous prompt engineering (Variant 4), the model was highly accurate and generally refused to hallucinate information or ignore user constraints.

**b. Limitations of the Hybrid RAG Workflow:**

1. **Inefficient Metadata Filtering:** The current hybrid retriever relies entirely on text/vector similarity to find constraints like "under $30". If the text "$25" doesn't mathematically bubble to the top of the search scores, the LLM will never see the product, making hard constraints difficult to enforce.
2. **Context Window / Top-K Bottleneck:** We are currently passing only the Top 5 documents to the LLM. If the absolute best product for a highly complex query was ranked #6 by the RRF algorithm, the LLM is completely blind to it and will confidently recommend a sub-optimal product.

**c. Suggestions for Improving Workflow Performance:**

To solve the metadata limitation, we could add explicit UI filters to our Streamlit app (e.g., a "Maximum Price" slider or a "Brand" dropdown). We could filter the underlying dataset for these hard constraints *before* passing the remaining products to the vector search, guaranteeing the LLM only sees items within budget. To solve the top-k bottleneck, we could simply increase our retrieval limit from 5 to 10 or 15 documents. While this would slightly increase the LLM's processing time, it gives the model a much broader pool of context to pull the perfect recommendation from.
