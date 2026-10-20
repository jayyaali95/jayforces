from collections import defaultdict, deque


class RateLimiter:
    """Sliding window limiter: at most `limit` requests per `window` seconds."""

    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.hits = defaultdict(deque)

    def _trim(self, q, now):
        while q and q[0] <= now - self.window:
            q.popleft()

    def allow(self, user, now):
        q = self.hits[user]
        self._trim(q, now)
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True

    def retry_after(self, user, now):
        q = self.hits[user]
        self._trim(q, now)
        return 0.0 if len(q) < self.limit else q[0] + self.window - now


class MultiLimiter:
    """Endpoint specific limits with a '*' fallback."""

    def __init__(self, rules):
        self.rules = rules
        self.limiters = {}

    def check(self, user, endpoint, now):
        rule = self.rules.get(endpoint, self.rules.get("*"))
        if rule is None:
            return True, 0.0
        lim = self.limiters.setdefault(endpoint, RateLimiter(*rule))
        wait = lim.retry_after(user, now)
        if wait > 0:
            return False, float(wait)
        lim.allow(user, now)
        return True, 0.0
