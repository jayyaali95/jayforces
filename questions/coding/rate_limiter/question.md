---
title: Rate limiter
difficulty: medium
category: coding
tags: classes, deque, sliding window
---
Protect the ride request API. Time is passed in explicitly (seconds, float) so tests are deterministic.

## Part 1: Sliding window

Implement `RateLimiter(limit, window)`. `allow(user, now)` returns `True` if the user made fewer than `limit`
allowed requests in the half open window `(now - window, now]`, and records the request. Rejected requests
are **not** recorded. Each user is independent. Calls arrive with non decreasing `now`.

## Part 2: Per endpoint rules and retry hints

Real traffic has different limits per endpoint. Implement `MultiLimiter(rules)` where `rules` is
`{endpoint: (limit, window)}` and the special key `"*"` is the default for unknown endpoints
(if there is no `"*"`, unknown endpoints are always allowed).

`check(user, endpoint, now)` returns `(allowed, retry_after)`. `retry_after` is `0.0` when allowed, otherwise
the seconds until the oldest counted request leaves the window, so a retry at `now + retry_after` would succeed.
Counters are per `(user, endpoint)`, including endpoints that fall back to `"*"`.
