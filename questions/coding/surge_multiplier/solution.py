TIERS = [(3.0, 2.5), (2.0, 2.0), (1.5, 1.5), (1.2, 1.25)]


def multiplier(requests, drivers):
    """Return the surge multiplier for a zone."""
    if requests < 0 or drivers < 0:
        raise ValueError("negative counts")
    if drivers == 0:
        return 1.0 if requests == 0 else 2.5
    ratio = requests / drivers
    return next((m for floor, m in TIERS if ratio >= floor), 1.0)


def _step(cur, target, limit):
    return cur + max(-limit, min(limit, target - cur))


def update_zones(previous, reports):
    """Return new {zone: multiplier} moving at most 0.5 toward targets."""
    out = {}
    for zone, (req, drv) in reports.items():
        out[zone] = round(_step(previous.get(zone, 1.0), multiplier(req, drv), 0.5), 2)
    for zone, cur in previous.items():
        if zone not in reports:
            out[zone] = round(_step(cur, 1.0, 0.25), 2)
    return out
