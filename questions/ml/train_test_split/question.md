---
title: Train test split
difficulty: easy
category: ml
tags: numpy, randomness, sampling
---
Write a reproducible splitter. Use `rng = np.random.default_rng(seed)` exactly as described so results are deterministic.

## Part 1: Random split

Implement `train_test_split(X, y, test_size=0.25, seed=0)`:

1. `n = len(X)`, `n_test = ceil(test_size * n)` (like sklearn). Raise `ValueError` if `n_test` is 0 or equal to `n`, or lengths differ.
2. `perm = rng.permutation(n)`; the first `n_test` indices of `perm` are the test set, the rest train.
3. Return `X_train, X_test, y_train, y_test` as numpy arrays, in the order given by `perm`.

## Part 2: Stratified

Implement `stratified_split(X, y, test_size=0.25, seed=0)` keeping class proportions. For each class `c` in sorted order:
take its indices (ascending), shuffle them with `rng.permutation` (same `rng`, one call per class, in sorted class order),
and put the first `round(test_size * count_c)` in test (Python `round`). Concatenate the test indices class by class, same for
train, then return the four arrays like part 1. A class whose test share rounds to 0 contributes nothing to test.
