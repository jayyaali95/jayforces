import operator

OPS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt, "<=": operator.le,
       ">": operator.gt, ">=": operator.ge, "in": lambda a, b: a in b}
AGGS = {"count": len, "sum": sum, "min": min, "max": max, "avg": lambda xs: round(sum(xs) / len(xs), 2)}


class Query:
    """Immutable, chainable query over a list of dicts."""

    def __init__(self, rows, steps=(), group=None):
        self._rows, self._steps, self._group = rows, tuple(steps), group

    def _then(self, step, group=None):
        return Query(self._rows, self._steps + (step,), group)

    def where(self, field, op, value):
        if op not in OPS:
            raise ValueError(f"unknown op {op!r}")
        f = OPS[op]
        return self._then(lambda rows: [r for r in rows if field in r and f(r[field], value)])

    def select(self, *fields):
        return self._then(lambda rows: [{k: r.get(k) for k in fields} for r in rows])

    def order_by(self, field, desc=False):
        def step(rows):
            have = [r for r in rows if field in r]
            return sorted(have, key=lambda r: r[field], reverse=desc) + [r for r in rows if field not in r]
        return self._then(step)

    def limit(self, n):
        return self._then(lambda rows: rows[:n])

    def group_by(self, field):
        return Query(self._rows, self._steps, field)

    def agg(self, **specs):
        key = self._group

        def step(rows):
            groups = {}
            for r in rows:
                if key is None or key in r:
                    groups.setdefault(r[key] if key else None, []).append(r)
            out = []
            for k, rs in groups.items():
                row = {key: k} if key else {}
                for name, (src, fn) in specs.items():
                    row[name] = len(rs) if fn == "count" else AGGS[fn]([r[src] for r in rs if src in r])
                out.append(row)
            return out

        return self._then(step)

    def all(self):
        rows = [dict(r) for r in self._rows]
        for step in self._steps:
            rows = step(rows)
        return [dict(r) for r in rows]
