---
title: ROC AUC
difficulty: medium
category: ml
tags: metrics, ranking, numpy
---
Evaluate a fraud score without sklearn. `y` holds 0/1 labels, `scores` higher means more likely positive.

## Part 1: AUC by ranking

Implement `roc_auc(y, scores)`: the probability that a random positive gets a higher score than a random negative,
counting ties as half. Use average ranks (Mann Whitney U) so it is `O(n log n)`, not a double loop.
Raise `ValueError` if there are no positives or no negatives.

## Part 2: The curve

Implement `roc_curve(y, scores)` returning `(fpr, tpr, thresholds)` numpy arrays. Thresholds are the distinct scores in
decreasing order, with an extra first threshold `np.inf` (so the curve starts at `(0, 0)`). For each threshold `t`, predict positive
when `score >= t`. Then `auc_trapezoid(fpr, tpr)` computes the area with the trapezoid rule; on any input it must match `roc_auc`.
