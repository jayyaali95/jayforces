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

`transform(X)` projects centered data onto the components. Raise `ValueError` if `n_components` is not in `[1, d]`.

## Part 2: Reconstruction and choosing k

Add `inverse_transform(Z)` mapping back to the original space. Implement `choose_k(X, target=0.95)` returning the smallest k
whose cumulative explained variance ratio is `>= target`.
