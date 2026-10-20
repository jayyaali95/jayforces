---
title: Surge multiplier
difficulty: easy
category: coding
tags: business rules, dicts
---
Every minute each zone reports `requests` (riders asking) and `drivers` (idle drivers).

## Part 1: Multiplier from ratio

Implement `multiplier(requests, drivers)`:

| ratio = requests / drivers | multiplier |
|----------------------------|-----------:|
| below 1.2                  | 1.0        |
| 1.2 to below 1.5           | 1.25       |
| 1.5 to below 2.0           | 1.5        |
| 2.0 to below 3.0           | 2.0        |
| 3.0 and up                 | 2.5        |

With zero drivers: no requests gives `1.0`, otherwise `2.5`. Negative inputs raise `ValueError`.

## Part 2: Smooth updates

Riders hate whiplash. Implement `update_zones(previous, reports)`: `previous` is `{zone: multiplier}`,
`reports` is `{zone: (requests, drivers)}`. For each reported zone compute the target multiplier, then
move from the previous value toward the target by at most `0.5` per update. Zones missing from
`previous` start at `1.0`. Zones in `previous` without a report decay toward `1.0` by `0.25` per update.
Return a new dict; values rounded to 2 decimals.
