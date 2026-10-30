---
title: K nearest neighbors
difficulty: medium
category: ml
tags: numpy, knn, vectorization
---
Implement KNN from scratch with numpy. `X` and `y` (and the `X` passed to `predict`) may be array-likes such as lists; class labels may be any sortable type, e.g. strings. Distances must be computed in a vectorized way.

## Part 1: Classifier

Implement `KNNClassifier(k=3)` with `fit(X, y)` (stores data, returns `self`) and `predict(X)` returning a numpy array of labels.
Use euclidean distance. Neighbors with equal distance are ordered by their index in the training set (use a stable sort).
The prediction is the majority label among the k neighbors; ties go to the **smallest** label.
Raise `ValueError` if `k < 1` or `k > n_train` when predicting.

**Example**
```python
>>> X = np.array([[0], [1], [2], [10], [11]])
>>> y = np.array([0, 0, 0, 1, 1])
>>> KNNClassifier(k=3).fit(X, y).predict(np.array([[1.4], [9]]))
array([0, 1])
```

## Part 2: Weighted votes and regression

Add `weights="uniform"` option; with `"distance"` each neighbor votes with weight `1 / d`. If any neighbor has distance 0,
only the zero distance neighbors vote (uniformly). Ties still go to the smallest label.

Implement `KNNRegressor(k=3, weights="uniform")` predicting the (weighted) mean of neighbor targets with the same zero distance rule.

**Example**
```python
>>> Xtr, ytr = np.array([[0], [1], [3]]), np.array([0, 1, 1])
>>> KNNClassifier(k=3).fit(Xtr, ytr).predict(np.array([[0.1]]))
array([1])
>>> KNNClassifier(k=3, weights="distance").fit(Xtr, ytr).predict(np.array([[0.1]]))
array([0])
>>> reg = KNNRegressor(k=2, weights="distance").fit(X, np.array([0.0, 1, 2, 10, 11]))
>>> reg.predict(np.array([[1.0]]))  # zero distance neighbor wins
array([1.])
```
