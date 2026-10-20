---
title: Driver dispatch simulation
difficulty: hard
category: coding
tags: simulation, heap, tie breaking
---
Simulate a tiny dispatcher on a grid. Distance is Manhattan: `|x1 - x2| + |y1 - y2|`.

## Part 1: Nearest driver

Implement `nearest(drivers, rider)` where `drivers` is `{driver_id: (x, y)}` and `rider` is `(x, y)`.
Return the closest driver id, ties broken by the smallest id, or `None` if there are no drivers.

## Part 2: Time based simulation

Implement `simulate(drivers, requests)`. `drivers` is `{driver_id: (x, y)}`, all free at time 0.
`requests` is a list of `(request_id, t, pickup, dropoff)` in any order. Process requests in `t` order
(ties by request id). For each request, among drivers free at time `t`, pick the nearest to `pickup`
(ties by driver id). One grid unit takes one time unit to drive. The driver is busy until
`t + dist(driver, pickup) + dist(pickup, dropoff)` and then becomes free **at the dropoff location**.
A driver whose busy time ends exactly at `t` is free for that request.
If nobody is free, the request is unmatched.

Return `{request_id: (driver_id, pickup_time) or None}` where `pickup_time = t + dist(driver, pickup)`.
Must handle 10k requests and 1k drivers in a couple of seconds, so keep busy drivers in a heap.

## Part 3: Utilization

Implement `utilization(drivers, requests, horizon)` returning `{driver_id: busy_fraction}` over `[0, horizon)`,
rounded to 3 decimals, using the same simulation. Busy time past the horizon does not count.
