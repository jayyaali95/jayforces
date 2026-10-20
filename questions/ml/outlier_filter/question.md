---
title: Outlier filtering
difficulty: easy
category: ml
tags: numpy, statistics, data cleaning
---
GPS glitches produce absurd trip durations. Flag them before training.

## Part 1: Z-score and IQR

Implement `zscore_mask(x, threshold=3.0)` returning a boolean numpy array, `True` for values with
`|x - mean| / std > threshold` (population std). If std is 0, nothing is an outlier.

Implement `iqr_mask(x, k=1.5)` using `q1, q3 = np.percentile(x, [25, 75])` (default linear interpolation): outliers are
values `< q1 - k * iqr` or `> q3 + k * iqr`.

## Part 2: Robust and per group

Implement `mad_mask(x, threshold=3.5)` using the modified z-score `0.6745 * (x - median) / MAD` where
`MAD = median(|x - median|)`; if MAD is 0, flag values that differ from the median.

Implement `group_iqr_mask(values, groups, k=1.5)` that applies `iqr_mask` within each group separately (groups is an array of
labels aligned with values) and returns one boolean mask in the original order.
