import itertools


def _matches(pattern, topic):
    p, t = pattern.split("."), topic.split(".")
    if p[-1] == "#":
        return len(t) > len(p) - 1 and all(a in ("*", b) for a, b in zip(p[:-1], t))
    return len(p) == len(t) and all(a in ("*", b) for a, b in zip(p, t))


class EventBus:
    """In-process pub/sub with * and # wildcards."""

    def __init__(self):
        self.subs = {}
        self._ids = itertools.count()
        self._errors = []

    def subscribe(self, pattern, handler):
        token = next(self._ids)
        self.subs[token] = (pattern, handler)
        return token

    def unsubscribe(self, token):
        return self.subs.pop(token, None) is not None

    def publish(self, topic, payload):
        called = 0
        for pattern, handler in list(self.subs.values()):
            if _matches(pattern, topic):
                called += 1
                try:
                    handler(topic, payload)
                except Exception as e:
                    self._errors.append((topic, e))
        return called

    def errors(self):
        return list(self._errors)
