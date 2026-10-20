---
title: Pairwise distances
difficulty: easy
category: ml
tags: numpy, broadcasting, vectorization
---
Distance matrices power KNN, clustering and dedup. Write them **without Python loops** (they must handle 2000x2000 fast).

## Part 1: Euclidean

Implement `euclidean(A, B)` for `A` of shape `(n, d)` and `B` of shape `(m, d)`, returning `(n, m)` distances.
Use the expansion `|a|^2 + |b|^2 - 2 a.b` and clip tiny negatives to 0 before the square root.

## Part 2: Manhattan and cosine

Implement `manhattan(A, B)` (broadcasting is fine) and `cosine_similarity(A, B)`. Rows with zero norm have similarity `0`
with everything. Finally `top_k_similar(A, B, k)` returning an `(n, k)` int array of indices into `B` with the highest cosine
similarity per row of `A`, best first, ties broken by smaller index.
