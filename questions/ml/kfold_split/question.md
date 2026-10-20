---
title: K-fold split
difficulty: easy
category: ml
tags: cross validation, indexing
---
Implement cross validation splits by hand, no sklearn.

## Part 1: Fold sizes

Implement `kfold_indices(n, k)` returning a list of `k` lists of indices. Indices `0..n-1` are taken in order;
the first `n % k` folds get one extra item (this matches sklearn's `KFold` without shuffle).
Raise `ValueError` if `k < 2` or `k > n`.

```python
kfold_indices(7, 3)  # [[0, 1, 2], [3, 4], [5, 6]]
```

## Part 2: Train / validation pairs

Implement `kfold_splits(n, k)` returning a list of `(train, val)` tuples, one per fold, where `val` is that fold and
`train` is every other index in increasing order.
