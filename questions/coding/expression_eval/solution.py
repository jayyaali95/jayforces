import re

_TOKEN = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)|([A-Za-z_]\w*)|(.))")
_FUNCS = {"min": min, "max": max}


def _tokens(expr):
    out, pos = [], 0
    expr = expr.rstrip()
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        num, name, op = m.groups()
        if num:
            out.append(("num", float(num)))
        elif name:
            out.append(("name", name))
        elif op in "+-*/(),":
            out.append(("op", op))
        else:
            raise ValueError(f"unexpected {op!r}")
        pos = m.end()
    return out


class _Parser:
    def __init__(self, tokens, variables):
        self.t, self.i, self.vars = tokens, 0, variables

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, value=None):
        tok = self.peek()
        if tok[0] is None or (value is not None and tok[1] != value):
            raise ValueError(f"expected {value or 'more input'}")
        self.i += 1
        return tok

    def expr(self):
        val = self.term()
        while self.peek()[1] in ("+", "-"):
            val = val + self.term() if self.take()[1] == "+" else val - self.term()
        return val

    def term(self):
        val = self.unary()
        while self.peek()[1] in ("*", "/"):
            if self.take()[1] == "*":
                val *= self.unary()
            else:
                val /= self.unary()
        return val

    def unary(self):
        if self.peek()[1] == "-":
            self.take()
            return -self.unary()
        return self.atom()

    def atom(self):
        kind, val = self.take()
        if kind == "num":
            return val
        if kind == "name":
            if self.peek()[1] == "(":
                return self.call(val)
            if val not in self.vars:
                raise NameError(val)
            return float(self.vars[val])
        if val == "(":
            v = self.expr()
            self.take(")")
            return v
        raise ValueError(f"unexpected {val!r}")

    def call(self, name):
        if name not in _FUNCS:
            raise NameError(name)
        self.take("(")
        if self.peek()[1] == ")":
            raise ValueError(f"{name}() needs arguments")
        args = [self.expr()]
        while self.peek()[1] == ",":
            self.take()
            args.append(self.expr())
        self.take(")")
        return float(_FUNCS[name](args))


def evaluate(expr, variables=None):
    """Evaluate an arithmetic expression without eval."""
    p = _Parser(_tokens(expr), variables or {})
    if not p.t:
        raise ValueError("empty expression")
    val = p.expr()
    if p.i != len(p.t):
        raise ValueError("trailing input")
    return float(val)
