def _events(shifts):
    ev = []
    for s, e in shifts:
        if e > s:
            ev += [(s, 1), (e, -1)]
    return sorted(ev)  # at equal time -1 sorts before +1


def max_online(shifts):
    """Return the peak number of concurrent drivers."""
    cur = best = 0
    for _, d in _events(shifts):
        cur += d
        best = max(best, cur)
    return best


def gaps(shifts, k, day_start, day_end):
    """Return merged intervals within the day where fewer than k drivers are online."""
    clipped = [(max(s, day_start), min(e, day_end)) for s, e in shifts]
    ev = _events(clipped)
    out, cur, t, i = [], 0, day_start, 0
    while t < day_end:
        while i < len(ev) and ev[i][0] == t:
            cur += ev[i][1]
            i += 1
        nxt = ev[i][0] if i < len(ev) else day_end
        nxt = min(nxt, day_end)
        if cur < k and nxt > t:
            if out and out[-1][1] == t:
                out[-1] = (out[-1][0], nxt)
            else:
                out.append((t, nxt))
        t = nxt
    return out
