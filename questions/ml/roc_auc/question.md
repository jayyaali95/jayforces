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

**Example**
```python
>>> roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
0.75
>>> roc_auc([0, 1], [0.5, 0.5])   # a tie counts as half
0.5
```

## Part 2: The curve

Implement `roc_curve(y, scores)` returning `(fpr, tpr, thresholds)` numpy arrays. Thresholds are the distinct scores in
decreasing order, with an extra first threshold `np.inf` (so the curve starts at `(0, 0)`). For each threshold `t`, predict positive
when `score >= t`. Then `auc_trapezoid(fpr, tpr)` (which accepts array-likes such as lists) computes the area with the trapezoid rule; on any input it must match `roc_auc`.

**Example**
```python
>>> fpr, tpr, thresholds = roc_curve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
>>> thresholds
array([ inf, 0.8 , 0.4 , 0.35, 0.1 ])
>>> fpr
array([0. , 0. , 0.5, 0.5, 1. ])
>>> tpr
array([0. , 0.5, 0.5, 1. , 1. ])
>>> auc_trapezoid(fpr, tpr)
0.75
```
