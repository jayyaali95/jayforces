import heapq


def _graph(deps):
    jobs = set(deps) | {d for ds in deps.values() for d in ds}
    return {j: set(deps.get(j, ())) for j in jobs}


def _find_cycle(g):
    color, stack = {}, []

    def dfs(u):
        color[u] = 1
        stack.append(u)
        for v in sorted(g[u]):
            if color.get(v) == 1:
                return stack[stack.index(v):] + [v]
            if v not in color and (c := dfs(v)):
                return c
        color[u] = 2
        stack.pop()
        return None

    for j in sorted(g):
        if j not in color and (c := dfs(j)):
            return c


def run_order(deps):
    """Topological order with alphabetical tie breaking."""
    g = _graph(deps)
    users = {j: [] for j in g}
    for j, ds in g.items():
        for d in ds:
            users[d].append(j)
    left = {j: len(ds) for j, ds in g.items()}
    ready = [j for j in g if not left[j]]
    heapq.heapify(ready)
    order = []
    while ready:
        j = heapq.heappop(ready)
        order.append(j)
        for u in users[j]:
            left[u] -= 1
            if not left[u]:
                heapq.heappush(ready, u)
    if len(order) != len(g):
        raise ValueError("cycle: " + " -> ".join(_find_cycle(g)))
    return order


def stages(deps):
    """Group jobs into parallel stages."""
    g, level = _graph(deps), {}
    for j in run_order(deps):
        level[j] = 1 + max((level[d] for d in g[j]), default=-1)
    out = [[] for _ in range(max(level.values(), default=-1) + 1)]
    for j in sorted(level):
        out[level[j]].append(j)
    return out


def _finish(deps, durations):
    g, end = _graph(deps), {}
    for j in run_order(deps):
        end[j] = max((end[d] for d in g[j]), default=0) + durations.get(j, 1)
    return g, end


def finish_time(deps, durations):
    """Wall time with unlimited workers."""
    return max(_finish(deps, durations)[1].values(), default=0)


def critical_path(deps, durations):
    """Longest chain of jobs, first to last."""
    g, end = _finish(deps, durations)
    if not end:
        return []
    best = max(end.values())
    cur = min(j for j in end if end[j] == best)
    path = [cur]
    while True:
        start = end[cur] - durations.get(cur, 1)
        prev = sorted(d for d in g[cur] if end[d] == start)
        if not prev:
            break
        cur = prev[0]
        path.append(cur)
    return path[::-1]
