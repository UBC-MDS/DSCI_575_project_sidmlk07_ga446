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

**Variant 3: The Final Factual Prompt (Chosen Prompt)**

- *Prompt:* We removed the misleading examples and added a strict `NO OUTSIDE KNOWLEDGE` clause. We explicitly commanded it to state "Price not listed" if the metadata was missing, and added a rule to exclude products if reviews mentioned negative side effects (e.g., "drying").
- *Result:* This prompt led to much better output. the LLM successfully identified negative constraints (warning the user that a product was "drying" for dry skin), it handled missing prices without guessing, and it strictly anchored its ingredient claims to the provided context block.

**Variant 4: The Hybrid Retrieval Refinement (Final Production Prompt)**

- *Prompt:* During our Step 3 Hybrid RAG testing, the model successfully found a product that matched "no white cast," but it failed the user's "mineral" constraint (recommending a chemical sunscreen instead). To fix this prioritization flaw, we updated Rule #5 to explicitly command: *"STRICT CONSTRAINTS: You must evaluate ALL adjectives in the user's query... If a product violates ANY of the requested constraints, you MUST NOT recommend it."*
- *Result:* The LLM successfully corrected its behavior. It learned to strictly enforce all adjectives (like "mineral" vs. "chemical") as non-negotiable filters, rather than ignoring one constraint just to satisfy another. If a perfect match could not be found, it honestly admitted it, resulting in a perfectly constrained final output.