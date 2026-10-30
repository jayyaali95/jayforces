import numpy as np


def euclidean(A, B):
    """(n, m) euclidean distances."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    sq = (A ** 2).sum(1)[:, None] + (B ** 2).sum(1)[None, :] - 2 * A @ B.T
    return np.sqrt(np.clip(sq, 0, None))


def manhattan(A, B):
    """(n, m) L1 distances."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    return np.abs(A[:, None, :] - B[None, :, :]).sum(-1)


def cosine_similarity(A, B):
    """(n, m) cosine similarity, 0 for zero rows."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    na, nb = np.linalg.norm(A, axis=1), np.linalg.norm(B, axis=1)
    denom = na[:, None] * nb[None, :]
    return np.divide(A @ B.T, denom, out=np.zeros_like(denom), where=denom > 0)


def top_k_similar(A, B, k):
    """Indices of the k most similar rows of B for each row of A."""
    s = cosine_similarity(A, B)
    return np.argsort(-s, axis=1, kind="stable")[:, :k]
