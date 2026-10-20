"""Runs one question's tests against the user's solution.py in the current dir.

Usage: python runner.py <tests.py> <unlocked_part> <seconds_per_test>
Prints one JSON line prefixed with RESULT: so stray prints can't confuse the server.
"""
import contextlib
import importlib.util
import io
import json
import re
import signal
import sys
import time
import traceback
from pathlib import Path


class Timeout(Exception):
    pass


def _alarm(*_):
    raise Timeout()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def user_trace():
    # Only keep frames from the user's file, that's the part they can fix.
    lines = traceback.format_exc().splitlines()
    start = next((i for i, ln in enumerate(lines) if 'solution.py", line' in ln), len(lines) - 1)
    lines = [re.sub(r'File ".*?solution.py"', 'File "solution.py"', ln) for ln in lines[start:]]
    return "\n".join(lines[-12:])


def main():
    tests_path, unlocked, per_test = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    sys.path[:0] = [str(Path.cwd()), str(Path(__file__).parent)]
    out = {"error": None, "stdout": "", "tests": []}
    buf = io.StringIO()

    tests = load("tests", tests_path)
    found = [(n, f) for n, f in vars(tests).items() if callable(f) and re.match(r"test_p\d+_", n)]

    sol = None
    try:
        with contextlib.redirect_stdout(buf):
            sol = load("solution", "solution.py")
    except BaseException:
        out["error"] = user_trace()

    signal.signal(signal.SIGALRM, _alarm)
    for name, fn in found:
        part = int(re.match(r"test_p(\d+)_", name).group(1))
        label = name.split("_", 2)[2].replace("_", " ").strip()
        row = {"name": label, "part": part, "ok": None, "msg": ""}
        out["tests"].append(row)
        if part > unlocked:
            continue  # locked: counts toward the total, not executed
        if sol is None:
            row.update(ok=False, msg="solution.py did not load, see the error above")
            continue
        t0 = time.perf_counter()
        signal.setitimer(signal.ITIMER_REAL, per_test)
        try:
            with contextlib.redirect_stdout(buf):
                fn(sol)
            row["ok"] = True
        except Timeout:
            row.update(ok=False, msg=f"timed out after {per_test:g}s")
        except AssertionError as e:
            row.update(ok=False, msg=str(e) or "assertion failed")
        except BaseException as e:
            text = str(e)
            row.update(ok=False, msg=(f"{type(e).__name__}: {text}" if text else type(e).__name__)[:600])
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        row["ms"] = round((time.perf_counter() - t0) * 1000, 1)

    out["stdout"] = buf.getvalue()[-4000:]
    sys.__stdout__.write("RESULT:" + json.dumps(out, default=str) + "\n")


if __name__ == "__main__":
    main()
