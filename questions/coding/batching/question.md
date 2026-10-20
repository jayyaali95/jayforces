---
title: Batching with generators
difficulty: easy
category: coding
tags: generators, iterators, itertools
---
We send events to a warehouse in batches. Inputs may be huge or endless, so everything must be lazy.

## Part 1: Fixed size batches

Implement generator `batched(iterable, size)` yielding lists of up to `size` items in order; the last batch may
be shorter, no empty batches. Raise `ValueError` if `size < 1` (raising when the generator is first advanced is fine).
It must work on infinite iterators: taking the first batch must not consume the whole input.

## Part 2: Weighted batches

The warehouse limits batches by bytes. Implement generator `batched_by_weight(iterable, max_weight, weight=len)`.
Fill a batch while the total weight stays `<= max_weight`. An item heavier than `max_weight` on its own is
sent alone in its own batch. Order is preserved.
