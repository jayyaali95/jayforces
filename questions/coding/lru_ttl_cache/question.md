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

**Example**
```python
>>> c = LRUCache(2)
>>> c.put("a", 1); c.put("b", 2)
>>> c.get("a")          # "a" is now most recently used
1
>>> c.put("c", 3)       # evicts "b"
>>> c.get("b")
None
>>> len(c)
2
```

## Part 2: Time to live

Implement `TTLCache(capacity, ttl)`. Methods take an explicit clock: `put(key, value, now)` and `get(key, now)`.
An entry expires at `put_time + ttl` (expired when `now >= expiry`) and reads as a miss. Reads do **not** extend
the TTL but do refresh LRU order. On `put` when full, first drop every expired entry, then evict LRU if still needed.
Also add `stats()` returning `{"hits": h, "misses": m}`.

**Example**
```python
>>> t = TTLCache(2, ttl=10)
>>> t.put("a", 1, now=0)
>>> t.get("a", now=5)
1
>>> t.get("a", now=10)   # expired when now >= 0 + 10
None
>>> t.stats()
{'hits': 1, 'misses': 1}
```
