---
title: LRU cache with TTL
difficulty: medium
category: coding
tags: classes, OrderedDict, design
---
We cache ETA lookups. Memory is limited and stale ETAs are worse than none.

## Part 1: LRU

Implement `LRUCache(capacity)` with `get(key)` (returns `None` on miss) and `put(key, value)`.
Both count as a use. When full, `put` of a new key evicts the least recently used key.
`len(cache)` returns the number of entries. `capacity < 1` raises `ValueError`. Both operations should be O(1).

## Part 2: Time to live

Implement `TTLCache(capacity, ttl)`. Methods take an explicit clock: `put(key, value, now)` and `get(key, now)`.
An entry expires at `put_time + ttl` (expired when `now >= expiry`) and reads as a miss. Reads do **not** extend
the TTL but do refresh LRU order. On `put` when full, first drop every expired entry, then evict LRU if still needed.
Also add `stats()` returning `{"hits": h, "misses": m}`.
