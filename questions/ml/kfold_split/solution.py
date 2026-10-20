def kfold_indices(n, k):
    """Split range(n) into k contiguous folds, bigger folds first."""
    if k < 2 or k > n:
        raise ValueError("need 2 <= k <= n")
    size, extra = divmod(n, k)
    folds, start = [], 0
    for i in range(k):
        end = start + size + (i < extra)
        folds.append(list(range(start, end)))
        start = end
    return folds


def kfold_splits(n, k):
    """Return [(train_indices, val_indices)] for every fold."""
    folds = kfold_indices(n, k)
    return [([j for f in folds[:i] + folds[i + 1:] for j in f], fold) for i, fold in enumerate(folds)]
