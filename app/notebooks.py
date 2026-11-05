"""Notebook questions (kind: notebook): one Jupyter notebook plus a random dataset per attempt. Standard library only.

    make_data(question_dir, seed, dest)   writes train.csv / test.csv / info.json (runs dsgen in a subprocess)
    ensure(q, dest, seed)                 makes dest/notebook.ipynb from the question's starter, once
    grading_code(path)                    turns a saved notebook into a solution.py the normal test runner can load
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = {"auc": "roc_auc_score", "ap": "average_precision_score", "r2": "r2_score"}

SETUP = """import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, r2_score

pd.set_option("display.max_columns", 50)"""

LOADER = '''import sys
import traceback

try:
    import matplotlib
    matplotlib.use("Agg")
except Exception:
    pass
try:
    from IPython.display import display
except Exception:
    display = print

for _n, _src in enumerate(CELLS, 1):  # like "Restart and run all"; one broken cell must not hide the rest
    try:
        exec(compile(_src, "<cell %d>" % _n, "exec"), globals())
    except Exception:
        print("--- notebook cell %d raised ---" % _n)
        traceback.print_exc(file=sys.stdout)
'''


def available():
    import importlib.util
    return importlib.util.find_spec("jupyterlab") is not None


def make_data(qdir, seed, dest):
    code = "import sys, dsgen; dsgen.write(*sys.argv[1:])"
    p = subprocess.run([sys.executable, "-c", code, str(qdir), str(seed), str(dest)], cwd=HERE,
                       capture_output=True, text=True, timeout=120)
    if p.returncode:
        raise RuntimeError("Could not generate the dataset (needs numpy and pandas): " + p.stderr[-600:])


def _stubs(starter):
    tree = ast.parse(starter)
    tree.body = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
    return ast.unparse(tree)


def _cell(kind, text):
    cell = {"cell_type": kind, "metadata": {}, "source": text}
    return cell if kind == "markdown" else {**cell, "execution_count": None, "outputs": []}


def ensure(q, dest, seed):
    dest = Path(dest)
    path = dest / "notebook.ipynb"
    if path.exists():
        return path
    make_data(q.dir, seed, dest)
    info = json.loads((dest / "info.json").read_text())
    score = METRICS[info["metric"]]
    check = (f'if __name__ == "__main__":  # skipped when the app grades this notebook\n'
             f'    tr, va = train_test_split(train, test_size=0.25, random_state=0)\n'
             f'    p = fit_predict(tr, va.drop(columns=TARGET))\n'
             f'    print("{info["metric"]}:", {score}(va[TARGET], p))')
    cells = [
        _cell("markdown", f"# {q.title}\n\nThe statement and the contest timer are in the jayforces tab. Work here: run cells, explore, "
                          "break things.\n\nThe app grades the functions you define below. **Run tests** reads this notebook as last "
                          "saved (it autosaves every few seconds, `Ctrl+S` saves now) and runs it top to bottom like "
                          "*Restart and run all*, so keep cells you don't need cheap.\n\n"
                          f"Files next to this notebook: `train.csv` (has `{info['target']}`) and `test.csv` (features only, the "
                          "labels are hidden)."),
        _cell("code", SETUP),
        _cell("code", 'train = pd.read_csv("train.csv")\ntest = pd.read_csv("test.csv")\ntrain.shape, test.shape'),
        _cell("code", "train.info()\ntrain.head()"),
        _cell("code", _stubs(q.starter)),
        _cell("code", check),
    ]
    nb = {"cells": cells, "nbformat": 4, "nbformat_minor": 4,
          "metadata": {"kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}}}
    path.write_text(json.dumps(nb, indent=1))
    return path


def grading_code(path):
    nb = json.loads(Path(path).read_text())
    cells = []
    for c in nb.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        lines = []
        for ln in src.splitlines():
            body = ln.lstrip()
            lines.append(ln[:len(ln) - len(body)] + "pass  # " + body if body.startswith(("%", "!")) else ln)  # magics
        cells.append("\n".join(lines))
    return LOADER.replace("CELLS", repr(cells), 1)
