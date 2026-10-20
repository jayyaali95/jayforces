---
title: Naive Bayes
difficulty: medium
category: ml
tags: probability, numpy, text classification
---
Classify support tickets as `billing`, `safety` or `app` from word counts.

## Part 1: Multinomial NB

Implement `MultinomialNB(alpha=1.0)`. `fit(X, y)` with `X` a non negative count matrix `(n, d)` stores:

- `classes_`: sorted unique labels (numpy array)
- `class_log_prior_[c] = log(count_c / n)`
- `feature_log_prob_[c, j] = log((N_cj + alpha) / (N_c + alpha * d))` where `N_cj` sums feature j over class c rows and `N_c = sum_j N_cj`

`predict_log_joint(X)` returns `X @ feature_log_prob_.T + class_log_prior_`; `predict(X)` returns the argmax class (first on ties).

## Part 2: Gaussian NB and probabilities

Add `predict_proba(X)` to `MultinomialNB` returning normalized probabilities computed stably from the log joint (log-sum-exp).

Implement `GaussianNB(var_smoothing=1e-9)` with per class `theta_` (means) and `var_` (population variances plus
`var_smoothing * max(variance of each feature over all of X)`), the same `classes_` and `class_log_prior_`, and `predict(X)` using
the Gaussian log likelihood `-0.5 * sum(log(2*pi*var) + (x - mean)^2 / var)`.
