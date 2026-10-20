---
title: Decision stump
difficulty: medium
category: ml
tags: trees, impurity, search
---
A decision stump is a one split tree. It is the building block of gradient boosting.

## Part 1: Impurity

Implement `gini(y)` = `1 - sum(p_c^2)` and `entropy(y)` = `-sum(p_c * log2(p_c))` over class frequencies. Empty input gives `0.0`.

## Part 2: Best split

Implement `best_split(X, y, criterion="gini")` returning `(feature, threshold, gain)` for the split `X[:, f] <= threshold`
that maximizes `gain = impurity(parent) - (n_left/n) * impurity(left) - (n_right/n) * impurity(right)`.
Candidate thresholds are midpoints between consecutive distinct sorted values of each feature. Ties (gain within `1e-12`):
smallest feature index, then smallest threshold. If no split has positive gain return `None`.

Then `class Stump` with `fit(X, y)` storing `feature_`, `threshold_`, `left_`, `right_` (majority class of each side, smallest label on ties)
and `predict(X)`. If there is no useful split, predict the overall majority class everywhere (`feature_` is `None`).
