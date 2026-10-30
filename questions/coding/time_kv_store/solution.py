import bisect

_DELETED = object()


class TimeStore:
    """Versioned key/value store."""

    def __init__(self):
        self.ts = {}
        self.vals = {}

    def _put(self, key, value, ts):
        times, vals = self.ts.setdefault(key, []), self.vals.setdefault(key, [])
        i = bisect.bisect_left(times, ts)
        if i < len(times) and times[i] == ts:
            vals[i] = value
        else:
            times.insert(i, ts)
            vals.insert(i, value)

    def set(self, key, value, ts):
        self._put(key, value, ts)

    def delete(self, key, ts):
        self._put(key, _DELETED, ts)

    def get(self, key, ts):
        times = self.ts.get(key, [])
        i = bisect.bisect_right(times, ts) - 1
        if i < 0 or self.vals[key][i] is _DELETED:
            return None
        return self.vals[key][i]

    def history(self, key, start, end):
        times = self.ts.get(key, [])
        lo, hi = bisect.bisect_left(times, start), bisect.bisect_right(times, end)
        return [(times[i], self.vals[key][i]) for i in range(lo, hi) if self.vals[key][i] is not _DELETED]

    def keys_at(self, ts):
        return sorted(k for k in self.ts if self.get(k, ts) is not None)
