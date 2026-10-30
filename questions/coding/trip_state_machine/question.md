---
title: Trip state machine
difficulty: medium
category: coding
tags: state machine, events, validation
---
A trip moves through states. Allowed transitions:

```python
TRANSITIONS = {
    "REQUESTED": {"ACCEPTED", "CANCELLED"},
    "ACCEPTED": {"ARRIVED", "CANCELLED"},
    "ARRIVED": {"STARTED", "CANCELLED"},
    "STARTED": {"COMPLETED"},
    "COMPLETED": set(),
    "CANCELLED": set(),
}
```

Every trip starts in `REQUESTED` the moment it exists.

## Part 1: One trip

Implement `class Trip` with `state` attribute starting at `"REQUESTED"`, `can(new_state)` and `apply(new_state)`.
`apply` moves to the new state or raises `ValueError` for an illegal or unknown transition (state unchanged).

**Example**
```python
>>> t = Trip()
>>> t.can("ACCEPTED")
True
>>> t.apply("ACCEPTED")
>>> t.state
'ACCEPTED'
>>> t.apply("COMPLETED")   # raises ValueError, state stays 'ACCEPTED'
```

## Part 2: Replaying a stream

Implement `replay(events)` for events `{"id": e, "trip": t, "state": s, "ts": n}` from many trips, in any order.
Process in `ts` order (stable). Skip events whose `id` was already processed (duplicates). Apply each event
to its trip; illegal transitions are rejected and do not change state. The first event for a trip implicitly
creates it in `REQUESTED` (an explicit `"REQUESTED"` event for a new trip is accepted and does nothing).
Return `{"states": {trip: state}, "rejected": [event ids in processing order]}`.

**Example**
```python
>>> events = [
...     {"id": "e1", "trip": "t1", "state": "ACCEPTED", "ts": 1},
...     {"id": "e2", "trip": "t1", "state": "COMPLETED", "ts": 2},   # illegal from ACCEPTED
...     {"id": "e1", "trip": "t1", "state": "ACCEPTED", "ts": 1},    # duplicate id, skipped
...     {"id": "e3", "trip": "t1", "state": "ARRIVED", "ts": 3},
...     {"id": "e4", "trip": "t2", "state": "CANCELLED", "ts": 1},
... ]
>>> replay(events)
{'states': {'t1': 'ARRIVED', 't2': 'CANCELLED'}, 'rejected': ['e2']}
```
