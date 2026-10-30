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

**Example**
```python
>>> edges = [("A", "B", 5), ("A", "C", 2), ("C", "B", 2), ("B", "D", 1), ("C", "D", 9)]
>>> fastest(edges, "A", "D")
5
>>> fastest(edges, "D", "A")   # unreachable
>>> fastest(edges, "A", "A")
0
```

## Part 2: Route

Implement `route(edges, src, dst)` returning `(minutes, [nodes])` for a fastest path, or `None`.
If several fastest paths exist, return the one whose node list is lexicographically smallest.
Parallel edges may exist; use the cheapest.

**Example**
```python
>>> route(edges, "A", "D")     # same edges as above
(5, ['A', 'C', 'B', 'D'])
```

## Part 3: Closures and stops

Implement `route_avoiding(edges, src, dst, closed)` where `closed` is a set of nodes that cannot be visited
(if `src` or `dst` is closed, return `None`), and `route_via(edges, src, stops, dst)` that must visit the stops in the
given order. Return `(minutes, [nodes])` concatenating the legs (do not repeat the joining nodes), or `None`.

**Example**
```python
>>> route_avoiding(edges, "A", "D", {"C"})   # same edges as above
(6, ['A', 'B', 'D'])
>>> route_via(edges, "A", ["C"], "D")
(5, ['A', 'C', 'B', 'D'])
```
