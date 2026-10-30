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

**Example**
```python
>>> sc = StandardScaler()
>>> sc.fit_transform([[1, 10], [3, 10]])   # second column is constant, so its std is treated as 1
array([[-1.,  0.],
       [ 1.,  0.]])
>>> sc.mean_, sc.std_
(array([ 2., 10.]), array([1., 1.]))
```

## Part 2: Inverse and missing values

Add `inverse_transform(Z)` undoing the scaling (calling it before `fit` also raises `RuntimeError`). Then make `fit` ignore `NaN` values when computing statistics
(use `np.nanmean` / `np.nanstd`); `transform` keeps `NaN` as `NaN`. A column that is entirely `NaN` gets mean `0` and std `1`.

**Example**
```python
>>> sc = StandardScaler().fit([[1, 10], [3, 10]])
>>> sc.inverse_transform([[-1, 0], [1, 0]])
array([[ 1., 10.],
       [ 3., 10.]])
>>> nan = float("nan")
>>> sc = StandardScaler().fit([[1, nan], [3, 4], [nan, 8]])   # NaNs are ignored when fitting
>>> sc.mean_, sc.std_
(array([2., 6.]), array([1., 2.]))
>>> sc.transform([[1, nan], [3, 4], [nan, 8]])   # NaN stays NaN
array([[-1., nan],
       [ 1., -1.],
       [nan,  1.]])
```
