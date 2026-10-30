---
title: Fluent query builder
difficulty: hard
category: coding
tags: design, fluent api, python
---
Analysts want to slice in-memory trip rows (list of dicts) without pandas. Build a small, immutable, chainable query object.

## Part 1: Filter, select, order, limit

Implement `Query(rows)` with methods that each return a **new** `Query` (the original is never changed):

- `where(field, op, value)` with ops `== != < <= > >= in`. Rows missing the field never match. Unknown ops raise `ValueError`.
- `select(*fields)` keeps only those keys (missing keys become `None`).
- `order_by(field, desc=False)` stable sort (ties keep their original relative order in both ascending and descending); rows missing the field go last in both directions.
- `limit(n)`.
- `all()` returns the result as a list of new dicts (in the order the methods were called).

**Example**
```python
>>> rows = [{"city": "sf", "fare": 10, "mi": 2},
...         {"city": "nyc", "fare": 30, "mi": 5},
...         {"city": "sf", "fare": 20, "mi": 4}]
>>> Query(rows).where("fare", ">=", 20).order_by("fare", desc=True).select("city", "fare").limit(2).all()
[{'city': 'nyc', 'fare': 30}, {'city': 'sf', 'fare': 20}]
```

## Part 2: Group by

Add `group_by(field)` followed by `agg(**specs)` where each spec is `(source_field, fn)` with fn one of `count sum avg min max`.
`agg` returns a new `Query` whose rows are `{field: key, name: value, ...}` ordered by first appearance of the key.
`avg` is rounded to 2 decimals. `count` counts rows (source field ignored, use `None`). Rows missing the group field are
skipped. Calling `agg` without `group_by` aggregates everything into one row with no key field.

**Example**
```python
# using the same rows as in Part 1
>>> Query(rows).group_by("city").agg(trips=(None, "count"), avg_fare=("fare", "avg"), max_mi=("mi", "max")).all()
[{'city': 'sf', 'trips': 2, 'avg_fare': 15.0, 'max_mi': 4}, {'city': 'nyc', 'trips': 1, 'avg_fare': 30.0, 'max_mi': 5}]
>>> Query(rows).agg(total=("fare", "sum")).all()
[{'total': 60}]
```
