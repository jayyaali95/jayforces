---
title: Vehicle booking calendar
difficulty: hard
category: coding
tags: intervals, sorted structures, design
---
Fleet partners book rental cars by the hour. A booking is half open `[start, end)` with `start < end`;
anything else raises `ValueError`.

## Part 1: Single car

Implement `Calendar` with `book(start, end)` returning `True` and storing the booking if it does not overlap any
existing booking, else `False`. Bookings that only touch (`[1, 3)` and `[3, 5)`) do not overlap. Also
`bookings()` returning the sorted list of `(start, end)`. 2000 bookings should take well under a second.

**Example**
```python
>>> cal = Calendar()
>>> cal.book(1, 3), cal.book(3, 5), cal.book(2, 4)
(True, True, False)
>>> cal.bookings()
[(1, 3), (3, 5)]
```

## Part 2: Overbooking buffer

Ops allows a small overbooking buffer. Implement `PoolCalendar(cars)` where at most `cars` bookings may overlap at
any moment. `book(start, end)` returns `True` and stores it only if that stays true; otherwise `False` and nothing is stored.

**Example**
```python
>>> pool = PoolCalendar(2)
>>> pool.book(1, 5), pool.book(2, 6), pool.book(3, 4), pool.book(5, 7)
(True, True, False, True)
```

## Part 3: Cancel and free slots

Add `cancel(start, end)` to both calendars: remove one booking equal to `(start, end)`, return `True`, or `False` if
there is none. Add `free(day_start, day_end)` to `Calendar` returning the sorted gaps inside the range not covered by a booking.

**Example**
```python
>>> cal.cancel(1, 3), cal.cancel(1, 3)   # cal from Part 1
(True, False)
>>> cal.free(0, 8)
[(0, 3), (5, 8)]
```
