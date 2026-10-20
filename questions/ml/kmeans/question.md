---
title: K-means clustering
difficulty: hard
category: ml
tags: numpy, clustering, vectorization
---
Cluster pickup locations into zones. Everything vectorized over points.

## Part 1: Lloyd's algorithm

Implement `kmeans(X, init, max_iter=100, tol=1e-6)` where `init` is a `(k, d)` array of starting centroids. Repeat:

1. assign each point to its nearest centroid (euclidean, ties go to the lower centroid index)
2. move each centroid to the mean of its points; a centroid with **no points stays where it is**
3. stop when no centroid moved more than `tol` (euclidean) or after `max_iter` iterations

Return `(centroids, labels, n_iter)` where `labels` match the final centroids (recompute assignment after the last update) and
`n_iter` counts update steps performed.

## Part 2: Inertia and k-means++

Implement `inertia(X, centroids, labels)` (sum of squared distances to the assigned centroid).

Implement `kmeans_pp_init(X, k, seed=0)` with `rng = np.random.default_rng(seed)`: pick the first centroid as `X[rng.integers(len(X))]`,
then repeatedly compute each point's squared distance `D` to its nearest chosen centroid and pick the next as
`X[rng.choice(len(X), p=D / D.sum())]`. Return a `(k, d)` array.
