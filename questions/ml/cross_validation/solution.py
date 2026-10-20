import itertools

import numpy as np


def _accuracy(t, p):
    return float(np.mean(np.asarray(t) == np.asarray(p)))


def _folds(n, k):
    size, extra = divmod(n, k)
    out, start = [], 0
    for i in range(k):
        end = start + size + (i < extra)
        out.append(np.arange(start, end))
        start = end
    return out


def cross_val_score(make, X, y, k=5, metric=None, params=None):
    """Score a fresh model on each of k contiguous folds."""
    X, y = np.asarray(X), np.asarray(y)
    metric, params = metric or _accuracy, params or {}
    scores = []
    for val in _folds(len(X), k):
        train = np.setdiff1d(np.arange(len(X)), val)
        model = make(**params)
        model.fit(X[train], y[train])
        scores.append(float(metric(y[val], model.predict(X[val]))))
    return scores


def stratified_folds(y, k):
    """Deal each class round robin across folds."""
    y = np.asarray(y)
    folds, i = [[] for _ in range(k)], 0
    for c in np.unique(y):
        for idx in np.flatnonzero(y == c):
            folds[i % k].append(int(idx))
            i += 1
    return [sorted(f) for f in folds]


def grid_search(make, grid, X, y, k=5, metric=None):
    """Exhaustive search over the grid using cross_val_score."""
    keys = sorted(grid)
    best = None
    for combo in itertools.product(*(grid[key] for key in keys)):
        params = dict(zip(keys, combo))
        score = float(np.mean(cross_val_score(make, X, y, k, metric, params)))
        if best is None or score > best[1]:
            best = (params, score)
    return best
