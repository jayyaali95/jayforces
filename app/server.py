"""pitstop: a small contest server. Standard library only.

    python app/server.py        -> http://localhost:8000
"""
import json
import mimetypes
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from questions import load_all

HERE = Path(__file__).resolve().parent
QDIR = Path(os.environ.get("QUESTIONS_DIR", HERE.parent / "questions"))
DATA = Path(os.environ.get("DATA_DIR", HERE.parent / "data"))
MINUTES = int(os.environ.get("CONTEST_MINUTES", 90))
LINEUP = ["easy", "medium", "medium", "hard"]

SCHEMA = """
create table if not exists contests (
    id integer primary key, started_at real, ends_at real, ended_at real);
create table if not exists attempts (
    contest_id integer, idx integer, slug text, code text,
    part integer default 1, best real default 0, runs integer default 0, solved_at real,
    primary key (contest_id, idx));
"""


def db():
    con = sqlite3.connect(DATA / "pitstop.db")
    con.row_factory = sqlite3.Row
    return con


class ApiError(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status = status


# ---------- contest logic ----------

def pick_lineup(con, bank):
    seen = {r["slug"]: r["n"] for r in con.execute("select slug, count(*) n from attempts group by slug")}
    best = None
    for _ in range(30):  # a few shuffles to get both coding and ML in the mix
        chosen = []
        for level in LINEUP:
            pool = [q for q in bank.values() if q.difficulty == level and q.slug not in chosen]
            if not pool:
                raise ApiError(400, f"Need more {level} questions in {QDIR} to build a contest.")
            fewest = min(seen.get(q.slug, 0) for q in pool)
            chosen.append(random.choice([q for q in pool if seen.get(q.slug, 0) == fewest]).slug)
        best = chosen
        if len({bank[s].category for s in chosen}) > 1:
            break
    return best


def close_expired(con):
    con.execute("update contests set ended_at = ends_at where ended_at is null and ends_at < ?", (time.time(),))
    con.commit()


def view(con, cid, bank):
    c = con.execute("select * from contests where id = ?", (cid,)).fetchone()
    if not c:
        raise ApiError(404, "No such contest.")
    qs, unlocked = [], True
    for a in con.execute("select * from attempts where contest_id = ? order by idx", (cid,)):
        q = bank.get(a["slug"])
        qs.append({**(q.summary() if q else {"slug": a["slug"], "title": a["slug"], "parts": 1}),
                   "idx": a["idx"], "best": a["best"], "part": a["part"], "runs": a["runs"],
                   "solved": a["solved_at"] is not None, "open": unlocked})
        unlocked = unlocked and a["solved_at"] is not None
    score = round(sum(q["best"] for q in qs) / max(len(qs), 1), 1)
    return {"id": c["id"], "started_at": c["started_at"], "ends_at": c["ends_at"],
            "ended_at": c["ended_at"], "active": c["ended_at"] is None, "score": score,
            "questions": qs, "now": time.time()}


def attempt(con, cid, idx, bank, need_open=True):
    v = view(con, cid, bank)
    if not 0 <= idx < len(v["questions"]):
        raise ApiError(404, "No such question in this contest.")
    if need_open and not v["questions"][idx]["open"]:
        raise ApiError(403, "Solve the previous question first.")
    a = con.execute("select * from attempts where contest_id = ? and idx = ?", (cid, idx)).fetchone()
    q = bank.get(a["slug"])
    if not q:
        raise ApiError(410, f"Question {a['slug']} is no longer in the bank.")
    return v, a, q


def run_tests(q, code, part):
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "solution.py").write_text(code)
        try:
            p = subprocess.run([sys.executable, str(HERE / "runner.py"), str(q.tests), str(part), str(q.timeout)],
                               cwd=tmp, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return {"error": "The whole run took over 120s and was stopped.", "tests": [], "stdout": ""}
    line = next((ln for ln in reversed(p.stdout.splitlines()) if ln.startswith("RESULT:")), None)
    if not line:
        return {"error": (p.stderr or "Runner crashed without output.")[-2000:], "tests": [], "stdout": p.stdout[-2000:]}
    return json.loads(line[7:])


# ---------- routes ----------

def r_state(con, bank, body):
    close_expired(con)
    row = con.execute("select id from contests where ended_at is null order by id desc limit 1").fetchone()
    counts = {}
    for q in bank.values():
        counts.setdefault(q.category, {}).setdefault(q.difficulty, 0)
        counts[q.category][q.difficulty] += 1
    return {"contest": view(con, row["id"], bank) if row else None, "bank": counts, "minutes": MINUTES}


def r_new(con, bank, body):
    close_expired(con)
    con.execute("update contests set ended_at = ? where ended_at is null", (time.time(),))
    slugs = pick_lineup(con, bank)
    now = time.time()
    cid = con.execute("insert into contests (started_at, ends_at) values (?, ?)", (now, now + MINUTES * 60)).lastrowid
    for i, s in enumerate(slugs):
        con.execute("insert into attempts (contest_id, idx, slug, code) values (?, ?, ?, ?)", (cid, i, s, bank[s].starter))
    con.commit()
    return view(con, cid, bank)


def r_end(con, bank, body, cid):
    con.execute("update contests set ended_at = ? where id = ? and ended_at is null", (time.time(), int(cid)))
    con.commit()
    return view(con, int(cid), bank)


def r_question(con, bank, body, cid, idx):
    v, a, q = attempt(con, int(cid), int(idx), bank)
    shown = q.parts[:a["part"]]
    locked = [re.sub(r"^## ", "", p.splitlines()[0]) for p in q.parts[a["part"]:]]
    return {**v["questions"][int(idx)], "intro": q.intro, "sections": shown, "locked": locked,
            "code": a["code"], "starter": q.starter}


def r_save(con, bank, body, cid, idx):
    v, a, q = attempt(con, int(cid), int(idx), bank)
    if v["active"]:
        con.execute("update attempts set code = ? where contest_id = ? and idx = ?", (body.get("code", ""), int(cid), int(idx)))
        con.commit()
    return {"saved": v["active"]}


def r_run(con, bank, body, cid, idx):
    cid, idx = int(cid), int(idx)
    close_expired(con)
    v, a, q = attempt(con, cid, idx, bank)
    if not v["active"]:
        raise ApiError(409, "This contest is over. Generate a new one to keep going.")
    code = body.get("code", "")
    res = run_tests(q, code, a["part"])
    tests = res["tests"]
    ran = [t for t in tests if t["ok"] is not None]
    passed = sum(1 for t in ran if t["ok"])
    pct = round(100 * passed / len(tests), 1) if tests else 0.0
    part, solved, new_part = a["part"], a["solved_at"], False
    if ran and passed == len(ran) and not res["error"]:
        if part < len(q.parts):
            part, new_part = part + 1, True
        elif passed == len(tests):
            solved = solved or time.time()
    con.execute("update attempts set code = ?, part = ?, best = max(best, ?), runs = runs + 1, solved_at = ? "
                "where contest_id = ? and idx = ?", (code, part, pct, solved, cid, idx))
    if solved and all(r["solved_at"] for r in con.execute("select solved_at from attempts where contest_id = ?", (cid,))):
        con.execute("update contests set ended_at = ? where id = ?", (time.time(), cid))
    con.commit()
    return {**res, "pct": pct, "passed": passed, "total": len(tests), "part": part,
            "new_part": new_part, "solved": bool(solved), "contest": view(con, cid, bank)}


def r_history(con, bank, body):
    close_expired(con)
    ids = [r["id"] for r in con.execute("select id from contests where ended_at is not null order by id desc limit 50")]
    return [view(con, i, bank) for i in ids]


ROUTES = [
    ("GET", r"/api/state", r_state),
    ("POST", r"/api/contests", r_new),
    ("GET", r"/api/history", r_history),
    ("POST", r"/api/contests/(\d+)/end", r_end),
    ("GET", r"/api/contests/(\d+)/q/(\d+)", r_question),
    ("PUT", r"/api/contests/(\d+)/q/(\d+)/code", r_save),
    ("POST", r"/api/contests/(\d+)/q/(\d+)/run", r_run),
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, ctype="application/json"):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _handle(self, method):
        path = self.path.split("?")[0]
        if method == "GET" and not path.startswith("/api/"):
            f = (HERE / "static" / (path.lstrip("/") or "index.html")).resolve()
            if not f.is_file() or HERE / "static" not in f.parents:
                f = HERE / "static" / "index.html"
            return self._send(200, f.read_bytes(), mimetypes.guess_type(f.name)[0] or "text/plain")
        for m, pattern, fn in ROUTES:
            match = re.fullmatch(pattern, path)
            if m == method and match:
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                    body = json.loads(self.rfile.read(n) or b"{}") if n else {}
                    con = db()
                    try:
                        return self._send(200, fn(con, load_all(QDIR), body, *match.groups()))
                    finally:
                        con.close()
                except ApiError as e:
                    return self._send(e.status, {"error": str(e)})
        self._send(404, {"error": "Not found."})

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PUT(self):
        self._handle("PUT")

    def log_message(self, fmt, *args):
        if "/code" not in self.path:  # autosave is noisy
            sys.stderr.write(f"{self.command} {self.path} {args[1] if len(args) > 1 else ''}\n")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    with db() as con:
        con.executescript(SCHEMA)
    port = int(os.environ.get("PORT", 8000))
    print(f"pitstop on http://localhost:{port}  ({len(load_all(QDIR))} questions, data in {DATA})")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
