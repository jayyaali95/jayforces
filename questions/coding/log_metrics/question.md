---
title: Log metrics
difficulty: easy
category: coding
tags: parsing, strings, robustness
---
An API gateway writes one line per request:

```
2024-05-01T10:00:00Z GET /rides 200 123ms
```

Fields are separated by one or more spaces: timestamp, method, path, status code, latency.
Some lines are corrupted (missing fields, non numeric status, latency without `ms`, blank lines).
A line is valid only if it has exactly 5 fields, the method is one of `GET POST PUT DELETE`,
the path starts with `/`, the status is a 3 digit integer between 100 and 599, and latency is a
non negative integer followed by `ms`.

## Part 1: Parse and count

Implement `parse_line(line)` returning a dict `{"ts", "method", "path", "status", "ms"}` (status and ms as int)
or `None` for invalid lines. Then `status_counts(lines)` returning `{status: count}` over valid lines.

## Part 2: Per endpoint latency

Implement `endpoint_stats(lines)` returning `{(method, path): {"count": n, "avg_ms": a, "p50_ms": m, "error_rate": e}}`.
`avg_ms` is a float rounded to 2 decimals, `p50_ms` is the lower median (sorted latencies, index `(n - 1) // 2`),
and `error_rate` is the share of status `>= 500`, rounded to 4 decimals. Query strings are not part of the path:
`/rides?id=3` counts as `/rides`.
