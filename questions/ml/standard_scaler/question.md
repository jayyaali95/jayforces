---
title: Standard scaler
difficulty: easy
category: ml
tags: numpy, preprocessing, broadcasting
---
Feature scaling with numpy, vectorized (no Python loops over rows).

## Part 1: Fit and transform

Implement `StandardScaler` with `fit(X)` (stores per column `mean_` and population `std_`, i.e. `ddof=0`; returns `self`),
`transform(X)` returning `(X - mean_) / std_`, and `fit_transform(X)`. Columns with zero std must not divide by
zero: treat their std as `1`. Calling `transform` before `fit` raises `RuntimeError`. Inputs are 2D arrays; do not modify them.

## Part 2: Inverse and missing values

Add `inverse_transform(Z)` undoing the scaling. Then make `fit` ignore `NaN` values when computing statistics
(use `np.nanmean` / `np.nanstd`); `transform` keeps `NaN` as `NaN`. A column that is entirely `NaN` gets mean `0` and std `1`.
