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

**Example**
```python
>>> enc = OneHotEncoder().fit(["car", "bike", "car"])
>>> enc.categories_
['bike', 'car']
>>> enc.transform(["bike", "car"])
array([[1., 0.],
       [0., 1.]])
>>> enc.transform(["scooter"])
Traceback (most recent call last):
ValueError: ...
```

## Part 2: Unknowns and decoding

Add constructor option `OneHotEncoder(handle_unknown="error")`; with `"ignore"`, unseen values become an all zero row.
Add `inverse_transform(M)` returning a list of categories using the argmax of each row; an all zero row maps to `None`.
Add `min_frequency=1`: categories seen fewer times than this during `fit` are dropped from `categories_` (and therefore
treated as unknown).

**Example**
```python
>>> enc = OneHotEncoder(handle_unknown="ignore", min_frequency=2)
>>> enc.fit(["car", "bike", "car", "scooter", "car", "bike"]).categories_  # scooter seen once, dropped
['bike', 'car']
>>> M = enc.transform(["bike", "scooter", "car"])
>>> M
array([[1., 0.],
       [0., 0.],
       [0., 1.]])
>>> enc.inverse_transform(M)
['bike', None, 'car']
```
