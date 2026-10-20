---
title: Driver shift coverage
difficulty: medium
category: coding
tags: intervals, sweep line, sorting
---
Drivers sign up for shifts `(start, end)` in minutes since midnight, half open `[start, end)`.

## Part 1: Peak

Implement `max_online(shifts)` returning the largest number of drivers online at the same moment.
A shift ending at `t` and another starting at `t` do not overlap. Shifts with `end <= start` are ignored.

## Part 2: Coverage gaps

Ops needs at least `k` drivers online at every moment of the day `[day_start, day_end)`.
Implement `gaps(shifts, k, day_start, day_end)` returning a sorted list of merged `(start, end)` intervals
inside the day where fewer than `k` drivers are online. Shifts may extend past the day; clip them.
