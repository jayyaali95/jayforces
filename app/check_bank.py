"""Sanity check for the question bank. Run it after adding a question:

    docker compose run --rm pitstop python app/check_bank.py [slug ...]

For every question: the reference solution must pass 100%, the derived starter
must load and fail, and there should be at least 15 tests.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from questions import load_all  # noqa: E402
from server import QDIR, run_tests  # noqa: E402


def main(only):
    bank = load_all(QDIR)
    bad = 0
    for slug, q in sorted(bank.items(), key=lambda kv: (kv[1].category, kv[1].difficulty, kv[0])):
        if only and slug not in only:
            continue
        n = len(q.parts)
        ref = run_tests(q, (q.dir / "solution.py").read_text(), n)
        fails = [t for t in ref["tests"] if not t["ok"]]
        start = run_tests(q, q.starter, n)
        problems = []
        if ref["error"]:
            problems.append("solution error: " + ref["error"].splitlines()[-1])
        if fails:
            problems.append(f"solution fails {len(fails)}: " + "; ".join(f"{t['name']}: {t['msg'][:120]}" for t in fails[:3]))
        if start["error"]:
            problems.append("starter does not load: " + start["error"].splitlines()[-1])
        if any(t["ok"] for t in start["tests"]):
            problems.append("starter passes some tests (fine if intended)")
        if len(ref["tests"]) < 15:
            problems.append(f"only {len(ref['tests'])} tests")
        parts = {t["part"] for t in ref["tests"]}
        if parts != set(range(1, n + 1)):
            problems.append(f"test parts {sorted(parts)} vs {n} parts in question.md")
        hard = [p for p in problems if not p.startswith("starter passes")]
        bad += bool(hard)
        mark = "FAIL" if hard else "ok  "
        print(f"{mark} {q.category:6} {q.difficulty:6} {slug:28} {len(ref['tests']):3} tests  {' | '.join(problems)}")
    print(f"\n{len(bank)} questions, {bad} with problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
