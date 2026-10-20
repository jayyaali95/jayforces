---
title: Rider app sessions
difficulty: medium
category: coding
tags: grouping, sorting, analytics
---
The rider app logs `(user, ts, screen)` tuples, `ts` in seconds, in no particular order.
A **session** is a run of one user's events where each gap between consecutive events is at most
`gap` seconds (default 1800). A bigger gap starts a new session.

## Part 1: Sessionize

Implement `sessionize(events, gap=1800)` returning `{user: [[(ts, screen), ...], ...]}` with sessions
in time order and events inside each session sorted by ts (stable for equal ts).

## Part 2: Funnel stats

Implement `session_stats(events, gap=1800)` returning a dict:

- `"sessions"`: total number of sessions
- `"avg_length"`: average session duration (last ts minus first ts) rounded to 1 decimal, `0.0` if none
- `"conversion"`: share of sessions where a `"request_ride"` screen appears **after** a `"set_destination"` screen
  in the same session, rounded to 3 decimals
