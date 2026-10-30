---
title: Cross validation and grid search
difficulty: medium
category: ml
tags: model selection, design, numpy
---
Models in these tests follow a tiny protocol: a factory `make(**params)` returns a fresh object with `fit(X, y)` and `predict(X)`.

## Part 1: cross_val_score

Implement `cross_val_score(make, X, y, k=5, metric=None, params=None)`: split indices `0..n-1` into k contiguous folds
(first `n % k` folds get one extra), and for each fold train a **fresh** model `make(**params)` on the other folds and score it on
this fold. `metric(y_true, y_pred)` defaults to accuracy. Return a list of k floats.

**Example**
```python
>>> class Majority:  # predicts the most common training label
...     def __init__(self): pass
...     def fit(self, X, y): self.m = np.bincount(y).argmax()
...     def predict(self, X): return np.full(len(X), self.m)
>>> X = [[i] for i in range(6)]
>>> cross_val_score(Majority, X, [0, 0, 0, 0, 1, 1], k=3)
[1.0, 1.0, 0.0]
```

## Part 2: Stratified folds and grid search

Implement `stratified_folds(y, k)`: for each class (sorted), deal its indices in increasing order round robin to folds
`0, 1, ..., k-1, 0, ...`, continuing the deal across classes from where the previous class stopped. Return a list of k sorted index lists.

Implement `grid_search(make, grid, X, y, k=5, metric=None)`: `grid` is `{param: [values]}`. Try every combination in
`itertools.product` order over **sorted** parameter names, score each with `cross_val_score` and return
`(best_params, best_mean_score)`. Ties keep the first combination. The `params` dict passed to `make` has its keys in sorted order.

**Example**
```python
>>> stratified_folds([0, 0, 0, 1, 1, 1], 3)
[[0, 3], [1, 4], [2, 5]]
>>> stratified_folds([0, 0, 0, 0, 1, 1], 2)
[[0, 2, 4], [1, 3, 5]]
>>> class Threshold:  # predicts 1 when x >= t
...     def __init__(self, t=0): self.t = t
...     def fit(self, X, y): pass
...     def predict(self, X): return (np.asarray(X)[:, 0] >= self.t).astype(int)
>>> grid_search(Threshold, {'t': [1, 3, 5]}, [[i] for i in range(6)], [0, 0, 0, 1, 1, 1], k=2)
({'t': 3}, 1.0)
```
