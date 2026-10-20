---
title: One hot encoder
difficulty: easy
category: ml
tags: encoding, numpy, categorical
---
Encode categorical features like `vehicle_type` for a model.

## Part 1: Encode

Implement `OneHotEncoder` with `fit(values)` learning the sorted unique categories into `categories_` (a list) and returning `self`,
and `transform(values)` returning a float numpy array of shape `(len(values), len(categories_))`.
An unseen category raises `ValueError` by default.

## Part 2: Unknowns and decoding

Add constructor option `OneHotEncoder(handle_unknown="error")`; with `"ignore"`, unseen values become an all zero row.
Add `inverse_transform(M)` returning a list of categories using the argmax of each row; an all zero row maps to `None`.
Add `min_frequency=1`: categories seen fewer times than this during `fit` are dropped from `categories_` (and therefore
treated as unknown).
