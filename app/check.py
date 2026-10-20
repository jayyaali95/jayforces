"""Tiny assertion helpers used by every questions/*/tests.py.

    from check import eq, close, raises, table

eq / close   compare and raise a readable AssertionError
raises       assert that a call blows up with a given exception
table        turn rows of (name, args, expected) into test functions
"""
import math
import re

try:
    import numpy as np
except ImportError:  # check.py must work without numpy too
    np = None


def _short(x, n=300):
    s = repr(x)
    return s if len(s) <= n else s[:n] + " ..."


def same(got, exp, tol=1e-6):
    if np is not None and (isinstance(got, np.ndarray) or isinstance(exp, np.ndarray)):
        g, e = np.asarray(got), np.asarray(exp)
        if g.shape != e.shape:
            return False
        if e.dtype.kind in "biufc" and g.dtype.kind in "biufc":
            return bool(np.allclose(g.astype(float), e.astype(float), atol=tol, rtol=tol, equal_nan=True))
        return bool(np.array_equal(g, e))
    if isinstance(exp, bool):
        bools = (bool,) if np is None else (bool, np.bool_)
        return isinstance(got, bools) and bool(got) == exp
    if isinstance(exp, float) or isinstance(got, float):
        try:
            return math.isclose(float(got), float(exp), rel_tol=tol, abs_tol=tol)
        except (TypeError, ValueError):
            return False
    if isinstance(exp, (list, tuple)) and isinstance(got, (list, tuple)):
        return type(got) is type(exp) and len(got) == len(exp) and all(same(a, b, tol) for a, b in zip(got, exp))
    if isinstance(exp, dict) and isinstance(got, dict):
        return got.keys() == exp.keys() and all(same(got[k], exp[k], tol) for k in exp)
    return got == exp


def eq(got, exp, tol=1e-6, msg=""):
    if not same(got, exp, tol):
        head = msg + "\n" if msg else ""
        raise AssertionError(f"{head}expected {_short(exp)}\n     got {_short(got)}")


def close(got, exp, tol=1e-4):
    eq(got, exp, tol)


def raises(exc, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc:
        return
    except Exception as e:
        raise AssertionError(f"expected {exc.__name__}, got {type(e).__name__}: {e}")
    raise AssertionError(f"expected {exc.__name__} to be raised, nothing was raised")


def table(ns, part, call, rows, tol=1e-6):
    """Register one test per row into the module namespace `ns`.

    call(sol, *args) produces the value; rows are (name, args, expected).
    If expected is an exception class, the call must raise it.
    """
    for name, args, exp in rows:
        args = args if isinstance(args, tuple) else (args,)
        slug = re.sub(r"\W+", "_", name.lower()).strip("_")
        key = f"test_p{part}_{slug}"
        while key in ns:
            key += "_"

        def test(sol, args=args, exp=exp):
            if isinstance(exp, type) and issubclass(exp, BaseException):
                raises(exp, call, sol, *args)
            else:
                eq(call(sol, *args), exp, tol)

        test.__name__ = key
        ns[key] = test
