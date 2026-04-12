import numpy as np


def precision_at_k(relevant: list[int], retrieved: list[int], k: int) -> float:
    """
    Precision@k: fraction of top-k retrieved docs that are relevant.

    Args:
        relevant: list of relevant document indices (ground truth)
        retrieved: list of retrieved document indices, ranked
        k: cutoff rank
    """
    retrieved_at_k = retrieved[:k]
    hits = len(set(retrieved_at_k) & set(relevant))
    return hits / k


def recall_at_k(relevant: list[int], retrieved: list[int], k: int) -> float:
    """
    Recall@k: fraction of relevant docs found in top-k results.
    """
    retrieved_at_k = retrieved[:k]
    hits = len(set(retrieved_at_k) & set(relevant))
    return hits / len(relevant) if relevant else 0.0


def reciprocal_rank(relevant: list[int], retrieved: list[int]) -> float:
    """
    Reciprocal Rank: 1/rank of the first relevant result.
    Used to compute MRR over multiple queries.
    """
    for rank, idx in enumerate(retrieved, start=1):
        if idx in relevant:
            return 1.0 / rank
    return 0.0


def mean_reciprocal_rank(
    relevant_list: list[list[int]], retrieved_list: list[list[int]]
) -> float:
    """
    MRR averaged over multiple queries.
    """
    rr_scores = [
        reciprocal_rank(rel, ret) for rel, ret in zip(relevant_list, retrieved_list)
    ]
    return float(np.mean(rr_scores))
