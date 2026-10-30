from collections import defaultdict


def _replay(events):
    """Walk events in time order. Returns shift/repair flags and per-car change log."""
    shift, repair = {}, {}
    changes = defaultdict(list)  # car -> [(ts, drivable)]
    for car, ev, ts in sorted(events, key=lambda e: e[2]):
        if ev == "OPEN":
            shift[car] = True
        elif ev == "CLOSE":
            shift[car] = False
        elif ev == "REPAIR_START":
            repair[car] = True
        elif ev == "REPAIR_END":
            repair[car] = False
        else:
            continue
        changes[car].append((ts, shift.get(car, False) and not repair.get(car, False)))
    return shift, repair, changes


def final_status(events):
    """Return {car_id: "OPEN" | "CLOSED" | "IN_REPAIR"}."""
    shift, repair, changes = _replay(events)
    return {car: "IN_REPAIR" if repair.get(car) else "OPEN" if shift.get(car) else "CLOSED" for car in changes}


def drivable_windows(events, car_id, until):
    """Return sorted, merged [(start, end)] windows where the car was drivable."""
    _, _, changes = _replay([e for e in events if e[2] < until])
    out, start = [], None

    def push(a, b):
        if b <= a:
            return
        if out and out[-1][1] == a:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))

    for ts, ok in changes.get(car_id, []):
        if ok and start is None:
            start = ts
        elif not ok and start is not None:
            push(start, ts)
            start = None
    if start is not None:
        push(start, until)
    return out


def available_at(events, t):
    """Return sorted car ids drivable at time t."""
    shift, repair, _ = _replay([e for e in events if e[2] <= t])
    return sorted(c for c in shift if shift[c] and not repair.get(c, False))
