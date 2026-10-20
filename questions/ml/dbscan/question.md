---
title: DBSCAN
difficulty: hard
category: ml
tags: clustering, graphs, bfs
---
Find hotspots of pickups with density based clustering. Distance is euclidean and "within eps" means `<= eps`.

## Part 1: Neighborhoods

Implement `neighbors(X, eps)` returning a list where item `i` is the sorted list of indices within `eps` of point `i`
(including `i` itself). Implement `core_mask(X, eps, min_samples)` returning a bool numpy array: a point is core if it has at
least `min_samples` neighbors (counting itself).

## Part 2: Clustering

Implement `dbscan(X, eps, min_samples)` returning int labels (`-1` for noise). Make it deterministic:

1. scan points in index order; an unvisited **core** point starts a new cluster (ids `0, 1, 2, ...`)
2. grow it breadth first using a FIFO queue, adding neighbors in increasing index order
3. border points (non core, within eps of a core point) take the cluster that reaches them first and are not expanded
4. points never reached are noise
