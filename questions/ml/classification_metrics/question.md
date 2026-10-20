---
title: Classification metrics
difficulty: easy
category: ml
tags: metrics, evaluation, numpy
---
Implement the evaluation metrics you'd otherwise import from sklearn. Inputs are lists or numpy arrays.

## Part 1: Binary metrics

Implement `binary_metrics(y_true, y_pred)` for labels in `{0, 1}` returning
`{"accuracy", "precision", "recall", "f1"}` as floats. When a metric's denominator is 0 it is `0.0`.
Raise `ValueError` for different lengths or empty input.

## Part 2: Multi class

Implement `confusion_matrix(y_true, y_pred, labels=None)` returning a numpy int array `M` where `M[i, j]` counts
true `labels[i]` predicted as `labels[j]`. If `labels` is `None`, use the sorted union of labels seen.
Implement `macro_f1(y_true, y_pred)`: the unweighted mean of per class F1 over that sorted union.
