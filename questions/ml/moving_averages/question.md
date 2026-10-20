---
title: Moving averages for demand
difficulty: easy
category: ml
tags: numpy, time series, smoothing
---
Smooth ride demand series before forecasting. Inputs are 1D sequences; return numpy float arrays.

## Part 1: Simple moving average

Implement `sma(x, window)` returning an array of length `len(x) - window + 1` where item `i` is the mean of
`x[i : i + window]`. Do it in O(n) with a cumulative sum (no loop over windows). Raise `ValueError` if `window < 1` or
`window > len(x)`.

## Part 2: Exponential and centered

Implement `ema(x, alpha)` with `ema[0] = x[0]` and `ema[t] = alpha * x[t] + (1 - alpha) * ema[t - 1]`; raise
`ValueError` unless `0 < alpha <= 1`. A loop over time is fine here.

Implement `rolling_zscore(x, window)` returning an array the same length as `x`: for `t < window - 1` the value is `nan`,
otherwise `(x[t] - mean) / std` over the trailing window `x[t - window + 1 : t + 1]` (population std). If that std is 0 the value is `0`.
