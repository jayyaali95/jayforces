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

**Example**
```python
Values rounded to 3 decimals.

>>> X = np.array([[2, 0], [3, 1], [0, 2], [1, 3]])
>>> y = np.array(["a", "a", "b", "b"])
>>> nb = MultinomialNB(alpha=1.0).fit(X, y)
>>> nb.classes_
array(['a', 'b'], dtype='<U1')
>>> nb.class_log_prior_.round(3)
array([-0.693, -0.693])
>>> nb.feature_log_prob_.round(3)
array([[-0.288, -1.386],
       [-1.386, -0.288]])
>>> nb.predict(np.array([[1, 0], [0, 1]]))
array(['a', 'b'], dtype='<U1')
```

## Part 2: Gaussian NB and probabilities

Add `predict_proba(X)` to `MultinomialNB` returning normalized probabilities computed stably from the log joint (log-sum-exp).

Implement `GaussianNB(var_smoothing=1e-9)` with per class `theta_` (means) and `var_` (population variances plus
`var_smoothing * max(variance of each feature over all of X)`), the same `classes_` and `class_log_prior_`, and `predict(X)` using
the Gaussian log likelihood `-0.5 * sum(log(2*pi*var) + (x - mean)^2 / var)`.

**Example**
```python
Values rounded to 3 decimals.

>>> nb.predict_proba(np.array([[1, 0]])).round(3)
array([[0.75, 0.25]])
>>> gnb = GaussianNB().fit(X.astype(float), y)
>>> gnb.theta_.round(3)
array([[2.5, 0.5],
       [0.5, 2.5]])
>>> gnb.var_.round(3)
array([[0.25, 0.25],
       [0.25, 0.25]])
>>> gnb.predict(np.array([[2.0, 1.0], [0.0, 3.0]]))
array(['a', 'b'], dtype='<U1')
```
