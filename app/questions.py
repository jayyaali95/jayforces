"""Loads the question bank from disk.

A question is a folder with:
    question.md   front matter + statement, split into "## Part N" sections
    solution.py   reference solution (the starter code is derived from it)
    tests.py      tests named test_p<part>_<name>(sol)
    starter.py    optional, overrides the derived starter
"""
import ast
import re
from pathlib import Path


def parse_md(text):
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.split(" #")[0].strip()  # allow trailing comments
        body = text[m.end():]
    chunks = re.split(r"^(?=## Part )", body, flags=re.M)
    intro = chunks[0].strip() if not chunks[0].startswith("## Part") else ""
    parts = [c.strip() for c in chunks if c.startswith("## Part")]
    return meta, intro, parts


def _stub(fn):
    body = []
    if fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(getattr(fn.body[0], "value", None), ast.Constant) \
            and isinstance(fn.body[0].value.value, str):
        body.append(fn.body[0])
    body.append(ast.parse("raise NotImplementedError").body[0])
    fn.body = body
    return fn


def _public(name):
    return not name.startswith("_") or (name.startswith("__") and name.endswith("__"))


def make_starter(src):
    """Keep imports, CONSTANTS, signatures and docstrings. Drop bodies and _helpers."""
    out = []
    for node in ast.parse(src).body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            out.append(ast.unparse(node))
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
            out.append(ast.unparse(node))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            out.append(ast.unparse(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _public(node.name):
            out.append(ast.unparse(_stub(node)))
        elif isinstance(node, ast.ClassDef) and _public(node.name):
            keep = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if _public(item.name):
                        keep.append(_stub(item))
                else:
                    keep.append(item)  # docstring, class attributes
            node.body = keep or [ast.Pass()]
            out.append(ast.unparse(node))
    code = ""
    for i, chunk in enumerate(out):
        is_import = chunk.startswith(("import ", "from "))
        prev_import = i and out[i - 1].startswith(("import ", "from "))
        code += ("\n" if is_import and prev_import else "\n\n\n") + chunk if i else chunk
    return code.strip() + "\n"


class Question:
    def __init__(self, folder: Path):
        self.dir = folder
        self.slug = folder.name
        meta, self.intro, self.parts = parse_md((folder / "question.md").read_text())
        self.title = meta.get("title", self.slug.replace("_", " ").capitalize())
        self.difficulty = meta.get("difficulty", "medium").lower()
        self.category = meta.get("category", "coding").lower()
        self.tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        self.timeout = float(meta.get("timeout", 3))
        self.tests = folder / "tests.py"

    @property
    def starter(self):
        own = self.dir / "starter.py"
        return own.read_text() if own.exists() else make_starter((self.dir / "solution.py").read_text())

    def summary(self):
        return {"slug": self.slug, "title": self.title, "difficulty": self.difficulty,
                "category": self.category, "tags": self.tags, "parts": len(self.parts)}


def load_all(root: Path):
    bank = {}
    for md in sorted(root.rglob("question.md")):
        try:
            q = Question(md.parent)
            bank[q.slug] = q
        except Exception as e:  # one broken question shouldn't take the app down
            print(f"skipping {md.parent}: {e}")
    return bank
