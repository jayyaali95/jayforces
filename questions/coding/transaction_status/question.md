---
title: Transaction status
difficulty: easy
category: coding
tags: events, dicts, sorting
---
Payments emit status events as dicts: `{"txn": "t1", "status": "AUTHORIZED", "ts": 3}`.
One transaction gets many events, they arrive in any order, and sometimes the same event shows up twice.

Known statuses, with a precedence used only to break timestamp ties:

```python
PRECEDENCE = {"CREATED": 0, "AUTHORIZED": 1, "CAPTURED": 2, "SETTLED": 3, "FAILED": 4, "REFUNDED": 5}
```

## Part 1: Final status

Implement `final_status(events)` returning `{txn: status}`. The status of a transaction is the
status of its event with the largest `ts`. When several events share the largest `ts`, pick the
one with the highest precedence. Events with an unknown status are ignored entirely.

## Part 2: Summary

Finance wants a quick summary. Implement `status_counts(events)` returning `{status: count}` of
final statuses (only statuses that occur), and `stuck(events, now, max_age)` returning a sorted
list of txn ids whose final status is not terminal (`SETTLED`, `FAILED`, `REFUNDED`) and whose
last event is older than `max_age`, meaning `now - last_ts > max_age`.
