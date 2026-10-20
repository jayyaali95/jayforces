import heapq


def _dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nearest(drivers, rider):
    """Return the closest driver id (ties by id) or None."""
    return min(drivers, key=lambda d: (_dist(drivers[d], rider), d), default=None)


def _run(drivers, requests):
    free = dict(drivers)  # id -> position
    busy = []  # (free_at, id, position)
    result, trips = {}, []
    for rid, t, pickup, dropoff in sorted(requests, key=lambda r: (r[1], r[0])):
        while busy and busy[0][0] <= t:
            _, d, pos = heapq.heappop(busy)
            free[d] = pos
        d = nearest(free, pickup)
        if d is None:
            result[rid] = None
            continue
        arrive = t + _dist(free.pop(d), pickup)
        done = arrive + _dist(pickup, dropoff)
        heapq.heappush(busy, (done, d, dropoff))
        result[rid] = (d, arrive)
        trips.append((d, t, done))
    return result, trips


def simulate(drivers, requests):
    """Return {request_id: (driver_id, pickup_time) or None}."""
    return _run(drivers, requests)[0]


def utilization(drivers, requests, horizon):
    """Return {driver_id: busy fraction of [0, horizon)}."""
    busy = {d: 0 for d in drivers}
    for d, start, end in _run(drivers, requests)[1]:
        busy[d] += max(0, min(end, horizon) - min(start, horizon))
    return {d: round(b / horizon, 3) for d, b in busy.items()}
