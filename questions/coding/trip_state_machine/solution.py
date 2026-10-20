TRANSITIONS = {
    "REQUESTED": {"ACCEPTED", "CANCELLED"},
    "ACCEPTED": {"ARRIVED", "CANCELLED"},
    "ARRIVED": {"STARTED", "CANCELLED"},
    "STARTED": {"COMPLETED"},
    "COMPLETED": set(),
    "CANCELLED": set(),
}


class Trip:
    """A single trip that only moves along legal transitions."""

    def __init__(self):
        self.state = "REQUESTED"

    def can(self, new_state):
        return new_state in TRANSITIONS.get(self.state, set())

    def apply(self, new_state):
        if not self.can(new_state):
            raise ValueError(f"{self.state} -> {new_state} is not allowed")
        self.state = new_state


def replay(events):
    """Replay an unordered event stream into final trip states."""
    trips, seen, rejected = {}, set(), []
    for e in sorted(events, key=lambda e: e["ts"]):
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        is_new = e["trip"] not in trips
        trip = trips.setdefault(e["trip"], Trip())
        if is_new and e["state"] == "REQUESTED":
            continue
        try:
            trip.apply(e["state"])
        except ValueError:
            rejected.append(e["id"])
    return {"states": {t: tr.state for t, tr in trips.items()}, "rejected": rejected}
