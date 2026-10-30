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

**Example**
```python
>>> euclidean([[0, 0], [3, 4]], [[0, 0], [6, 8], [3, 0]])
array([[ 0., 10.,  3.],
       [ 5.,  5.,  4.]])
```

## Part 2: Manhattan and cosine

Implement `manhattan(A, B)` (broadcasting is fine) and `cosine_similarity(A, B)`. Rows with zero norm have similarity `0`
with everything. Finally `top_k_similar(A, B, k)` returning an `(n, k)` int array of indices into `B` with the highest cosine
similarity per row of `A`, best first, ties broken by smaller index.

**Example**
```python
>>> manhattan([[0, 0], [3, 4]], [[0, 0], [6, 8], [3, 0]])
array([[ 0., 14.,  3.],
       [ 7.,  7.,  4.]])
>>> cosine_similarity([[1, 0], [0, 0]], [[1, 1], [0, 2], [2, 0]]).round(3)   # zero row -> all 0
array([[0.707, 0.   , 1.   ],
       [0.   , 0.   , 0.   ]])
>>> top_k_similar([[1, 0], [0, 0]], [[1, 1], [0, 2], [2, 0]], 2)   # row 2: all ties, smaller index first
array([[2, 0],
       [0, 1]])
```
