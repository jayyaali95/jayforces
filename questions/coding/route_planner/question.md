---
title: Route planner
difficulty: hard
category: coding
tags: graphs, dijkstra, heap
---
The road graph is a list of directed edges `(from, to, minutes)` with non negative minutes.

## Part 1: Fastest time

Implement `fastest(edges, src, dst)` returning the minimum travel time, `0` if `src == dst`, or `None` if unreachable.
Nodes that appear nowhere in the edges still exist only as themselves.

## Part 2: Route

Implement `route(edges, src, dst)` returning `(minutes, [nodes])` for a fastest path, or `None`.
If several fastest paths exist, return the one whose node list is lexicographically smallest.
Parallel edges may exist; use the cheapest.

## Part 3: Closures and stops

Implement `route_avoiding(edges, src, dst, closed)` where `closed` is a set of nodes that cannot be visited
(if `src` or `dst` is closed, return `None`), and `route_via(edges, src, stops, dst)` that must visit the stops in the
given order. Return `(minutes, [nodes])` concatenating the legs (do not repeat the joining nodes), or `None`.
