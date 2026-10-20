import bisect


def _check(start, end):
    if not start < end:
        raise ValueError("need start < end")


class Calendar:
    """One car: no overlaps allowed."""

    def __init__(self):
        self.items = []  # sorted (start, end)

    def book(self, start, end):
        _check(start, end)
        i = bisect.bisect_left(self.items, (start, end))
        if i > 0 and self.items[i - 1][1] > start:
            return False
        if i < len(self.items) and self.items[i][0] < end:
            return False
        self.items.insert(i, (start, end))
        return True

    def bookings(self):
        return list(self.items)

    def cancel(self, start, end):
        i = bisect.bisect_left(self.items, (start, end))
        if i < len(self.items) and self.items[i] == (start, end):
            del self.items[i]
            return True
        return False

    def free(self, day_start, day_end):
        out, t = [], day_start
        for s, e in self.items:
            if e <= t or s >= day_end:
                continue
            if s > t:
                out.append((t, s))
            t = max(t, e)
        if t < day_end:
            out.append((t, day_end))
        return out


class PoolCalendar:
    """`cars` identical cars: at most `cars` overlapping bookings."""

    def __init__(self, cars):
        self.cars = cars
        self.items = []

    def book(self, start, end):
        _check(start, end)
        ev = sorted([(s, 1) for s, e in self.items if s < end and e > start] +
                    [(e, -1) for s, e in self.items if s < end and e > start] + [(start, 1), (end, -1)])
        cur = 0
        for _, d in ev:
            cur += d
            if cur > self.cars:
                return False
        bisect.insort(self.items, (start, end))
        return True

    def bookings(self):
        return list(self.items)

    def cancel(self, start, end):
        if (start, end) in self.items:
            self.items.remove((start, end))
            return True
        return False
