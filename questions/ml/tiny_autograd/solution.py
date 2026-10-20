import math


class Value:
    """A scalar that records how it was computed."""

    def __init__(self, data, parents=(), backward=None):
        self.data = float(data)
        self.grad = 0.0
        self._parents = parents
        self._back = backward or (lambda: None)

    @staticmethod
    def _wrap(x):
        return x if isinstance(x, Value) else Value(x)

    def __add__(self, other):
        other = self._wrap(other)
        out = Value(self.data + other.data, (self, other))

        def back():
            self.grad += out.grad
            other.grad += out.grad
        out._back = back
        return out

    def __mul__(self, other):
        other = self._wrap(other)
        out = Value(self.data * other.data, (self, other))

        def back():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._back = back
        return out

    def __pow__(self, k):
        out = Value(self.data ** k, (self,))

        def back():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._back = back
        return out

    def _unary(self, value, local):
        out = Value(value, (self,))

        def back():
            self.grad += local * out.grad
        out._back = back
        return out

    def relu(self):
        return self._unary(max(self.data, 0.0), 1.0 if self.data > 0 else 0.0)

    def tanh(self):
        t = math.tanh(self.data)
        return self._unary(t, 1 - t * t)

    def exp(self):
        e = math.exp(self.data)
        return self._unary(e, e)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-self._wrap(other))

    def __truediv__(self, other):
        return self * self._wrap(other) ** -1

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return self._wrap(other) - self

    def __rtruediv__(self, other):
        return self._wrap(other) / self

    def _topo(self):
        order, seen, stack = [], set(), [(self, False)]
        while stack:
            node, done = stack.pop()
            if done:
                order.append(node)
            elif id(node) not in seen:
                seen.add(id(node))
                stack.append((node, True))
                stack.extend((p, False) for p in node._parents if id(p) not in seen)
        return order

    def backward(self):
        order = self._topo()
        self.grad = 1.0
        for node in reversed(order):
            node._back()

    def zero_grad(self):
        for node in self._topo():
            node.grad = 0.0

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
