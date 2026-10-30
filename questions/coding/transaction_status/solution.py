PRECEDENCE = {"CREATED": 0, "AUTHORIZED": 1, "CAPTURED": 2, "SETTLED": 3, "FAILED": 4, "REFUNDED": 5}
TERMINAL = {"SETTLED", "FAILED", "REFUNDED"}


def _latest(events):
    best = {}
    for e in events:
        if e["status"] not in PRECEDENCE:
            continue
        key = (e["ts"], PRECEDENCE[e["status"]])
        if e["txn"] not in best or key > best[e["txn"]][0]:
            best[e["txn"]] = (key, e["status"])
    return best


def final_status(events):
    """Return {txn: final status}."""
    return {t: s for t, (_, s) in _latest(events).items()}


def status_counts(events):
    """Return {status: number of transactions ending in it}."""
    out = {}
    for s in final_status(events).values():
        out[s] = out.get(s, 0) + 1
    return out


def stuck(events, now, max_age):
    """Return sorted txn ids that are not terminal and went quiet for over max_age."""
    return sorted(t for t, ((ts, _), s) in _latest(events).items() if s not in TERMINAL and now - ts > max_age)
