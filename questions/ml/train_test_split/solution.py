import math

import numpy as np


def train_test_split(X, y, test_size=0.25, seed=0):
    """Shuffle once with the seed and cut off the test set."""
    X, y = np.asarray(X), np.asarray(y)
    n = len(X)
    n_test = math.ceil(test_size * n)
    if len(y) != n or n_test == 0 or n_test >= n:
        raise ValueError("bad split sizes")
    perm = np.random.default_rng(seed).permutation(n)
    te, tr = perm[:n_test], perm[n_test:]
    return X[tr], X[te], y[tr], y[te]


def stratified_split(X, y, test_size=0.25, seed=0):
    """Split each class separately so proportions are preserved."""
    X, y = np.asarray(X), np.asarray(y)
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for c in np.unique(y):
        idx = np.flatnonzero(y == c)
        idx = idx[rng.permutation(len(idx))]
        k = round(test_size * len(idx))
        te.append(idx[:k])
        tr.append(idx[k:])
    tr, te = np.concatenate(tr), np.concatenate(te)
    return X[tr], X[te], y[tr], y[te]
