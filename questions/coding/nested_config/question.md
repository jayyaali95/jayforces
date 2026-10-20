---
title: Nested config
difficulty: medium
category: coding
tags: recursion, dicts, python
---
Service configs live as nested dicts in code and as flat `a.b.c` keys in env files. Convert between them.

## Part 1: Flatten

Implement `flatten(config, sep=".")` turning nested dicts into a flat dict with joined keys.
Lists and other values are leaves. An empty nested dict is kept as a leaf: `{"a": {}}` stays `{"a": {}}`.
Keys must be strings; raise `TypeError` otherwise. Raise `ValueError` if a key contains `sep`.

## Part 2: Unflatten and merge

Implement `unflatten(flat, sep=".")`, the inverse of flatten. If two keys conflict (`"a"` is a leaf and also has
child `"a.b"`), raise `ValueError`.

Implement `deep_merge(base, override)` returning a new dict: nested dicts merge recursively, anything else
in `override` replaces the value from `base`. Inputs must not be mutated, and the result must not share
nested dicts with the inputs.
