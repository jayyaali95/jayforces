---
title: Car fleet status
difficulty: medium
category: coding
tags: events, state, intervals
---
Every car in the fleet emits events as `(car_id, event, ts)` tuples. `ts` is an integer
timestamp. Events can arrive out of order, so always process them sorted by `ts`. When two
events share a timestamp, keep the order they had in the input.

| event          | meaning                                 |
|----------------|-----------------------------------------|
| `OPEN`         | the car starts its shift                |
| `CLOSE`        | the car ends its shift                  |
| `REPAIR_START` | a repair ticket is opened for the car   |
| `REPAIR_END`   | the repair ticket is closed             |

Anything else is noise and must be ignored. A car that has never sent a valid event does not exist.

## Part 1: Current status

Implement `final_status(events)` returning `{car_id: status}` after all events, where status is:

- `"IN_REPAIR"` if a repair ticket is open (this wins over everything else)
- `"OPEN"` if the shift is open
- `"CLOSED"` otherwise

```python
final_status([("c1", "OPEN", 1), ("c1", "CLOSE", 5), ("c2", "OPEN", 2)])
# {"c1": "CLOSED", "c2": "OPEN"}
```

## Part 2: When can it drive?

A car can be driven when its shift is open **and** no repair ticket is open.

Implement `drivable_windows(events, car_id, until)` returning the list of `(start, end)` windows,
sorted, where the car was drivable. Only events with `ts < until` matter, and a window still
going at `until` ends at `until`. Windows must be maximal: drop zero length windows and merge
windows that touch (`(0, 5)` and `(5, 9)` become `(0, 9)`). Unknown cars give `[]`.

```python
ev = [("c1", "OPEN", 0), ("c1", "REPAIR_START", 4), ("c1", "REPAIR_END", 6)]
drivable_windows(ev, "c1", 10)   # [(0, 4), (6, 10)]
```

## Part 3: Dispatch board

Dispatch needs to know who is drivable right now. Implement `available_at(events, t)` returning
a sorted list of car ids that are drivable after applying every event with `ts <= t`.
