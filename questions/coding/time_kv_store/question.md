---
title: Time travel key value store
difficulty: medium
category: coding
tags: classes, binary search, bisect
---
Driver profiles change over time and support needs to see what a value was at any moment.

## Part 1: Set and get at time

Implement `TimeStore` with `set(key, value, ts)` and `get(key, ts)` returning the value with the largest
timestamp `<= ts`, or `None`. Timestamps for a key may arrive **out of order**. Setting the same key and
timestamp again overwrites. Aim for `O(log n)` gets.

## Part 2: Deletes and history

Add `delete(key, ts)`: from `ts` on the key reads as missing, until a later `set`.
Add `history(key, start, end)` returning `[(ts, value)]` for all sets with `start <= ts <= end`, sorted by ts,
skipping deletes. Add `keys_at(ts)` returning a sorted list of keys that have a value at `ts`.
