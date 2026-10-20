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
- `order_by(field, desc=False)` stable sort; rows missing the field go last in both directions.
- `limit(n)`.
- `all()` returns the result as a list of new dicts (in the order the methods were called).

## Part 2: Group by

Add `group_by(field)` followed by `agg(**specs)` where each spec is `(source_field, fn)` with fn one of `count sum avg min max`.
`agg` returns a new `Query` whose rows are `{field: key, name: value, ...}` ordered by first appearance of the key.
`avg` is rounded to 2 decimals. `count` counts rows (source field ignored, use `None`). Rows missing the group field are
skipped. Calling `agg` without `group_by` aggregates everything into one row with no key field.
