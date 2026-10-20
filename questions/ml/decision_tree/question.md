---
title: Decision tree classifier
difficulty: hard
category: ml
tags: trees, recursion, design
---
Grow a CART style classification tree with gini impurity.

## Part 1: Fit and predict

Implement `DecisionTree(max_depth=None, min_samples_split=2)` with `fit(X, y)` and `predict(X)`.

At each node: if all labels are equal, depth reached `max_depth`, or the node has fewer than `min_samples_split` samples, make a leaf.
Otherwise find the best split exactly like this: for every feature, thresholds are midpoints between consecutive distinct sorted values;
gain is `gini(parent) - weighted gini(children)` for `x <= t` going left. Keep the highest gain, ties to the smaller feature then smaller
threshold (gain differences under `1e-12` count as ties). If no split has positive gain, make a leaf (yes, that means a
greedy tree cannot split XOR at the root). A leaf predicts the majority label
(smallest label on ties). The root is depth 0.

## Part 2: Introspection

Add `depth()` (a lone leaf has depth 0), `n_leaves()`, `predict_proba(X)` returning class frequencies at the reached leaf as an array
`(n, n_classes)` ordered by sorted `classes_`, and `feature_importances_` after fit: for each feature, the sum over its splits of
`n_node / n_total * gain`, normalized to sum to 1 (all zeros if the tree is a single leaf).
