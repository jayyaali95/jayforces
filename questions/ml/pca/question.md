---
title: PCA from scratch
difficulty: medium
category: ml
tags: numpy, linear algebra, dimensionality reduction
---
Compress GPS trace features with principal component analysis.

## Part 1: Fit and transform

Implement `PCA(n_components)` with `fit(X)` that centers the data, computes the covariance matrix with `ddof=1`,
and takes its top eigenvectors (`np.linalg.eigh`, then sort by eigenvalue descending). Store:

- `mean_` shape `(d,)`
- `components_` shape `(k, d)`, each row a unit vector. Fix the sign so the entry with the largest absolute value in each row is positive.
- `explained_variance_` (top k eigenvalues) and `explained_variance_ratio_` (divided by the sum of **all** eigenvalues)

`transform(X)` projects centered data onto the components. `fit` raises `ValueError` if `n_components` is not in `[1, d]`.

**Example**
```python
>>> pca = PCA(1).fit([[1, 1], [2, 2], [3, 3], [4, 4]])
>>> pca.mean_
array([2.5, 2.5])
>>> pca.components_.round(3)
array([[0.707, 0.707]])
>>> pca.explained_variance_.round(3), pca.explained_variance_ratio_.round(3)
(array([3.333]), array([1.]))
>>> pca.transform([[1, 1], [2, 2], [3, 3], [4, 4]]).round(3)
array([[-2.121],
       [-0.707],
       [ 0.707],
       [ 2.121]])
```

## Part 2: Reconstruction and choosing k

Add `inverse_transform(Z)` mapping back to the original space. Implement `choose_k(X, target=0.95)` returning the smallest k
whose cumulative explained variance ratio is `>= target`.

**Example**
```python
>>> X = [[1, 1], [2, 2], [3, 3], [4, 4]]
>>> pca = PCA(1).fit(X)
>>> pca.inverse_transform(pca.transform(X)).round(3)   # the data is exactly 1-D, so reconstruction is exact
array([[1., 1.],
       [2., 2.],
       [3., 3.],
       [4., 4.]])
>>> choose_k([[1, 2], [2, 4.1], [3, 5.9], [4, 8]], target=0.95)
1
>>> choose_k([[1, 0], [-1, 0], [0, 1], [0, -1]], target=0.95)   # ratios are 0.5 / 0.5
2
```
