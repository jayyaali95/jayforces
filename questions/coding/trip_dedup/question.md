---
title: Trip record dedup
difficulty: easy
category: coding
tags: dicts, sorting, data cleaning
---
Our trip pipeline replays records, so the same trip shows up several times with different
`version` numbers. Each record looks like:

```python
{"trip_id": "t1", "rider": "r1", "version": 2, "fare": 1250, "status": "COMPLETED"}
```

## Part 1: Keep the latest

Implement `dedup(records)` returning one record per `trip_id`: the one with the highest `version`.
If two records share the highest version, keep the one that appeared **last** in the input.
Return them sorted by `trip_id`. Do not mutate the input.

## Part 2: Rider summary

Implement `rider_summary(records)` using deduplicated records. Return
`{rider: {"trips": n, "spend": total_fare_of_completed, "cancel_rate": r}}` where `spend` sums `fare`
only for `COMPLETED` trips and `cancel_rate` is the share of `CANCELLED` trips rounded to 3 decimals.
