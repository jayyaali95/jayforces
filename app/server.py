"""jayforces: a small contest server. Standard library only.

    python app/server.py        -> http://localhost:8000
"""
import atexit
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

import notebooks
from questions import load_all

HERE = Path(__file__).resolve().parent
QDIR = Path(os.environ.get("QUESTIONS_DIR", HERE.parent / "questions"))
DATA = Path(os.environ.get("DATA_DIR", HERE.parent / "data"))
MINUTES = int(os.environ.get("CONTEST_MINUTES", 90))
LINEUP = ["easy", "medium", "medium", "hard"]
JUPYTER_PORT = int(os.environ.get("JUPYTER_PORT", 8888))
JUPYTER = {"port": None}  # set in main() once JupyterLab is running; notebook questions need it

SCHEMA = """
create table if not exists contests (
    id integer primary key, started_at real, ends_at real, ended_at real,
    paused_at real, paused_total real not null default 0);
create table if not exists attempts (
    contest_id integer, idx integer, slug text, code text,
    part integer default 1, best real default 0, runs integer default 0, solved_at real,
    primary key (contest_id, idx));
"""


def db():
    con = sqlite3.connect(DATA / "jayforces.db")
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
            pool = [q for q in bank.values() if q.difficulty == level and q.slug not in chosen
                    and (JUPYTER["port"] or not q.notebook)]
            if not pool:
                raise ApiError(400, f"Need more {level} questions in {QDIR} to build a contest.")
            fewest = min(seen.get(q.slug, 0) for q in pool)
            chosen.append(random.choice([q for q in pool if seen.get(q.slug, 0) == fewest]).slug)
        best = chosen
        if len({bank[s].category for s in chosen}) > 1:
            break
    return best


def close_expired(con):
    con.execute("update contests set ended_at = ends_at where ended_at is null and paused_at is null and ends_at <= ?", (time.time(),))
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
            "ended_at": c["ended_at"], "paused_at": c["paused_at"],
            "duration": c["ends_at"] - c["started_at"] - c["paused_total"],
            "active": c["ended_at"] is None, "score": score,
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


def nb_seed(cid, idx):
    return cid * 10 + idx


def nb_dir(cid, idx):
    return DATA / "notebooks" / f"c{cid}_q{idx}"


def run_tests(q, code, part, data_dir=None, seed=7):
    """data_dir: where a notebook question's train.csv / test.csv live (made on the fly if omitted)."""
    limit = 300 if q.notebook else 120
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "solution.py").write_text(code)
        env = {**os.environ, "MPLBACKEND": "Agg"}
        if q.notebook:
            if data_dir is None:
                data_dir = Path(tmp, "data")
                notebooks.make_data(q.dir, seed, data_dir)
            for name in ("train.csv", "test.csv"):
                shutil.copy(Path(data_dir, name), Path(tmp, name))
            env["JF_SEED"] = str(seed)
        try:
            p = subprocess.run([sys.executable, str(HERE / "runner.py"), str(q.tests), str(part), str(q.timeout)],
                               cwd=tmp, capture_output=True, text=True, timeout=limit, env=env)
        except subprocess.TimeoutExpired:
            return {"error": f"The whole run took over {limit}s and was stopped.", "tests": [], "stdout": ""}
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
    return {"contest": view(con, row["id"], bank) if row else None, "bank": counts, "minutes": MINUTES,
            "jupyter": JUPYTER["port"]}


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


def r_pause(con, bank, body, cid):
    close_expired(con)
    con.execute("update contests set paused_at = ? where id = ? and ended_at is null and paused_at is null",
                (time.time(), int(cid)))
    con.commit()
    return view(con, int(cid), bank)


def r_resume(con, bank, body, cid):
    close_expired(con)
    now = time.time()
    con.execute("update contests set ends_at = ends_at + (? - paused_at), "
                "paused_total = paused_total + (? - paused_at), paused_at = null "
                "where id = ? and ended_at is null and paused_at is not null",
                (now, now, int(cid)))
    con.commit()
    return view(con, int(cid), bank)


def r_question(con, bank, body, cid, idx):
    v, a, q = attempt(con, int(cid), int(idx), bank)
    shown = q.parts[:a["part"]]
    locked = [re.sub(r"^## ", "", p.splitlines()[0]) for p in q.parts[a["part"]:]]
    url = None
    if q.notebook:
        d = nb_dir(int(cid), int(idx))
        try:
            notebooks.ensure(q, d, nb_seed(int(cid), int(idx)))
        except Exception as e:
            raise ApiError(500, str(e))
        url = f"/doc/tree/{d.name}/notebook.ipynb"
    return {**v["questions"][int(idx)], "intro": q.intro, "sections": shown, "locked": locked,
            "code": a["code"], "starter": q.starter, "notebook": url}


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
    if q.notebook:  # the notebook on disk is the source of truth, not the editor
        d = nb_dir(cid, idx)
        try:
            code, res = a["code"], run_tests(q, notebooks.grading_code(notebooks.ensure(q, d, nb_seed(cid, idx))),
                                              a["part"], d, nb_seed(cid, idx))
        except Exception as e:
            raise ApiError(500, str(e))
    else:
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
    ("POST", r"/api/contests/(\d+)/pause", r_pause),
    ("POST", r"/api/contests/(\d+)/resume", r_resume),
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


def start_jupyter():
    """JupyterLab for the notebook questions, embedded by the page. Skipped if it isn't installed."""
    if not notebooks.available():
        print("jupyterlab not installed: notebook questions are left out of contests")
        return
    root = DATA / "notebooks"
    prefs = DATA / "jupyter-settings" / "@jupyterlab" / "docmanager-extension"
    prefs.mkdir(parents=True, exist_ok=True)
    root.mkdir(parents=True, exist_ok=True)
    (prefs / "plugin.jupyterlab-settings").write_text('{"autosave": true, "autosaveInterval": 5}')  # run-tests reads the saved file
    cmd = [sys.executable, "-m", "jupyterlab", "--no-browser", "--allow-root", "--ip=0.0.0.0", f"--port={JUPYTER_PORT}",
           f"--ServerApp.root_dir={root}", "--IdentityProvider.token=", "--ServerApp.password=",
           "--ServerApp.tornado_settings={'headers': {'Content-Security-Policy': 'frame-ancestors *'}}"]  # allow our iframe
    proc = subprocess.Popen(cmd, cwd=root, env={**os.environ, "JUPYTERLAB_SETTINGS_DIR": str(DATA / "jupyter-settings")},
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(proc.terminate)
    JUPYTER["port"] = JUPYTER_PORT


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    start_jupyter()
    with db() as con:
        con.executescript(SCHEMA)
        columns = {row["name"] for row in con.execute("pragma table_info(contests)")}
        if "paused_at" not in columns:
            con.execute("alter table contests add column paused_at real")
        if "paused_total" not in columns:
            con.execute("alter table contests add column paused_total real not null default 0")
    port = int(os.environ.get("PORT", 8000))
    print(f"jayforces on http://localhost:{port}  ({len(load_all(QDIR))} questions, data in {DATA})")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
