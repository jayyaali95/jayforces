---
title: Driver ratings
difficulty: easy
category: coding
tags: classes, deque, sorting
---
Riders rate drivers from 1 to 5 stars. Only recent ratings matter.

## Part 1: Rolling average

Implement a class `Ratings(window=100)`:

- `add(driver_id, stars)` records a rating. `stars` must be an `int` from 1 to 5, otherwise raise `ValueError`
  (note that `True` is not a rating).
- `average(driver_id)` returns the mean of that driver's last `window` ratings, rounded to 2 decimals, or `None` if they have none.

## Part 2: Leaderboard

Implement `top(k, min_ratings=1)` returning up to `k` driver ids with at least `min_ratings`
ratings in their window, sorted by average (high first), then by number of ratings in the window
(high first), then by driver id (ascending).
