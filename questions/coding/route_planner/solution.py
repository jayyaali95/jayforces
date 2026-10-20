import heapq


def _adj(edges, closed=frozenset()):
    g = {}
    for a, b, w in edges:
        if a in closed or b in closed:
            continue
        if w < g.setdefault(a, {}).get(b, float("inf")):
            g[a][b] = w
    return g


def _search(g, src, dst):
    # Heap of (time, path) gives lexicographically smallest path among equal times.
    heap, done = [(0, [src])], set()
    while heap:
        t, path = heapq.heappop(heap)
        node = path[-1]
        if node == dst:
            return t, path
        if node in done:
            continue
        done.add(node)
        for nxt, w in g.get(node, {}).items():
            if nxt not in done:
                heapq.heappush(heap, (t + w, path + [nxt]))
    return None


def fastest(edges, src, dst):
    """Minimum minutes from src to dst, or None."""
    r = _search(_adj(edges), src, dst)
    return r[0] if r else None


def route(edges, src, dst):
    """(minutes, path) of the fastest, lexicographically smallest path."""
    return _search(_adj(edges), src, dst)


def route_avoiding(edges, src, dst, closed):
    """Fastest route that never touches a closed node."""
    if src in closed or dst in closed:
        return None
    return _search(_adj(edges, frozenset(closed)), src, dst)


def route_via(edges, src, stops, dst):
    """Fastest route visiting stops in order."""
    g, total, path = _adj(edges), 0, [src]
    for a, b in zip([src] + list(stops), list(stops) + [dst]):
        leg = _search(g, a, b)
        if leg is None:
            return None
        total += leg[0]
        path += leg[1][1:]
    return total, path
