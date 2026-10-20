from check import table


def run(sol, ops):
    e = sol.Editor()
    out = None
    for op in ops:
        out = getattr(e, op[0])(*op[1:])
    return e.text, e.cursor, out


table(globals(), 1, run, [
    ("type", [("type", "hello")], ("hello", 5, None)),
    ("insert middle", [("type", "hllo"), ("move", -3), ("type", "e")], ("hello", 2, None)),
    ("backspace", [("type", "hello"), ("backspace", 2)], ("hel", 3, None)),
    ("backspace too many", [("type", "hi"), ("backspace", 10)], ("", 0, None)),
    ("delete forward", [("type", "hello"), ("home",), ("delete", 2)], ("llo", 0, None)),
    ("delete at end", [("type", "hi"), ("delete",)], ("hi", 2, None)),
    ("move clamps", [("type", "hi"), ("move", -10), ("move", 1)], ("hi", 1, None)),
    ("end", [("type", "abc"), ("home",), ("end",), ("type", "!")], ("abc!", 4, None)),
])
table(globals(), 2, run, [
    ("undo type", [("type", "a"), ("type", "b"), ("undo",)], ("a", 1, True)),
    ("undo restores cursor", [("type", "abc"), ("move", -2), ("backspace",), ("undo",)], ("abc", 1, True)),
    ("redo", [("type", "abc"), ("backspace",), ("undo",), ("redo",)], ("ab", 2, True)),
    ("nothing to undo", [("undo",)], ("", 0, False)),
    ("edit clears redo", [("type", "a"), ("undo",), ("type", "b"), ("redo",)], ("b", 1, False)),
    ("noop backspace not a step", [("type", "a"), ("home",), ("backspace",), ("undo",)], ("", 0, True)),
    ("moves are not steps", [("type", "ab"), ("move", -1), ("undo",)], ("", 0, True)),
    ("undo all then redo all", [("type", "a"), ("type", "b"), ("undo",), ("undo",), ("redo",), ("redo",)], ("ab", 2, True)),
])
table(globals(), 3, run, [
    ("selected text", [("type", "hello world"), ("select", 6, 11), ("selected",)], ("hello world", 11, "world")),
    ("type replaces selection", [("type", "hello world"), ("select", 11, 6), ("type", "lyft")], ("hello lyft", 10, None)),
    ("backspace removes selection", [("type", "abcdef"), ("select", 1, 4), ("backspace",)], ("aef", 1, None)),
    ("undo selection replace", [("type", "abcdef"), ("select", 1, 4), ("type", "X"), ("undo",)], ("abcdef", 6, True)),
    ("move clears selection", [("type", "abc"), ("select", 0, 3), ("move", 0), ("type", "!")], ("abc!", 4, None)),
    ("clamped selection", [("type", "abc"), ("select", -5, 99), ("delete",)], ("", 0, None)),
])
