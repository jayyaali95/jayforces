from collections import deque

import numpy as np


def neighbors(X, eps):
    """Sorted neighbor index lists, self included."""
    X = np.asarray(X, dtype=float)
    d = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    return [np.flatnonzero(row <= eps).tolist() for row in d]


def core_mask(X, eps, min_samples):
    """True for points with at least min_samples neighbors."""
    return np.array([len(n) >= min_samples for n in neighbors(X, eps)], dtype=bool)


def dbscan(X, eps, min_samples):
    """Deterministic DBSCAN labels."""
    nbrs = neighbors(X, eps)
    core = [len(n) >= min_samples for n in nbrs]
    labels = np.full(len(nbrs), -1)
    cluster = 0
    for i in range(len(nbrs)):
        if labels[i] != -1 or not core[i]:
            continue
        labels[i] = cluster
        queue = deque([i])
        while queue:
            p = queue.popleft()
            if not core[p]:
                continue
            for q in nbrs[p]:
                if labels[q] == -1:
                    labels[q] = cluster
                    queue.append(q)
        cluster += 1
    return labels
