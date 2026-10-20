from collections import defaultdict


def sessionize(events, gap=1800):
    """Group events into per-user sessions."""
    by_user = defaultdict(list)
    for user, ts, screen in sorted(events, key=lambda e: e[1]):
        by_user[user].append((ts, screen))
    out = {}
    for user, evs in by_user.items():
        sessions = [[evs[0]]]
        for prev, cur in zip(evs, evs[1:]):
            if cur[0] - prev[0] > gap:
                sessions.append([])
            sessions[-1].append(cur)
        out[user] = sessions
    return out


def _converted(session):
    seen_dest = False
    for _, screen in session:
        if screen == "set_destination":
            seen_dest = True
        elif screen == "request_ride" and seen_dest:
            return True
    return False


def session_stats(events, gap=1800):
    """Return session count, average length and conversion."""
    sessions = [s for ss in sessionize(events, gap).values() for s in ss]
    if not sessions:
        return {"sessions": 0, "avg_length": 0.0, "conversion": 0.0}
    return {"sessions": len(sessions),
            "avg_length": round(sum(s[-1][0] - s[0][0] for s in sessions) / len(sessions), 1),
            "conversion": round(sum(map(_converted, sessions)) / len(sessions), 3)}
