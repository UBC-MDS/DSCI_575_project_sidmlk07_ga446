# Milestone 2 - RAG Pipeline: Semantic and Hybrid Retrieval

## 1. Model Choice & Rationale:

For the LLM generator, we selected `meta-llama/Llama-3.2-3B-Instruct` to be used locally via Ollama. Since both of us have an Apple M4 chip with unified memory, this allows us to use this 3 billion parameter model to execute with high speed and low latency. We specifically opted for the "Instruct" variant, as our LangChain RAG pipeline requires the model to strictly adhere to formatting constraints and base its answers purely on retrieved context rather than its internal memory. We utilize the `langchain_ollama` wrapper to integrate it seamlessly into our pipeline.

---
