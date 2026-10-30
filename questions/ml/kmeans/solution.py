import numpy as np


def _assign(X, C):
    d = (X ** 2).sum(1)[:, None] + (C ** 2).sum(1)[None, :] - 2 * X @ C.T
    return d.argmin(1)


def kmeans(X, init, max_iter=100, tol=1e-6):
    """Lloyd's algorithm. Returns (centroids, labels, n_iter)."""
    X, C = np.asarray(X, dtype=float), np.array(init, dtype=float)
    n_iter = 0
    for _ in range(max_iter):
        labels = _assign(X, C)
        new = C.copy()
        for j in range(len(C)):
            members = X[labels == j]
            if len(members):
                new[j] = members.mean(0)
        n_iter += 1
        moved = np.linalg.norm(new - C, axis=1).max()
        C = new
        if moved <= tol:
            break
    return C, _assign(X, C), n_iter


def inertia(X, centroids, labels):
    """Sum of squared distances to assigned centroids."""
    X = np.asarray(X, dtype=float)
    return float(((X - np.asarray(centroids)[labels]) ** 2).sum())


def kmeans_pp_init(X, k, seed=0):
    """k-means++ seeding."""
    X = np.asarray(X, dtype=float)
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        D = ((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1).min(1)
        C.append(X[rng.choice(len(X), p=D / D.sum())])
    return np.array(C)
