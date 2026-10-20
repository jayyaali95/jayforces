class Editor:
    """Text buffer with cursor, undo/redo and selection."""

    def __init__(self):
        self.text, self.cursor = "", 0
        self.sel = None
        self.undo_stack, self.redo_stack = [], []

    def _commit(self, before, after_text, after_cursor):
        if after_text == before[0]:
            self.text, self.cursor = after_text, after_cursor
            return
        self.undo_stack.append((before, (after_text, after_cursor)))
        self.redo_stack.clear()
        self.text, self.cursor = after_text, after_cursor

    def _cut_selection(self):
        if self.sel is None:
            return self.text, self.cursor
        a, b = self.sel
        self.sel = None
        return self.text[:a] + self.text[b:], a

    def type(self, s):
        before = (self.text, self.cursor)
        text, cur = self._cut_selection()
        self._commit(before, text[:cur] + s + text[cur:], cur + len(s))

    def backspace(self, n=1):
        before, had_sel = (self.text, self.cursor), self.sel is not None
        text, cur = self._cut_selection()
        if not had_sel:
            k = min(n, cur)
            text, cur = text[:cur - k] + text[cur:], cur - k
        self._commit(before, text, cur)

    def delete(self, n=1):
        before, had_sel = (self.text, self.cursor), self.sel is not None
        text, cur = self._cut_selection()
        if not had_sel:
            text = text[:cur] + text[cur + n:]
        self._commit(before, text, cur)

    def move(self, k):
        self.sel = None
        self.cursor = max(0, min(len(self.text), self.cursor + k))

    def home(self):
        self.sel, self.cursor = None, 0

    def end(self):
        self.sel, self.cursor = None, len(self.text)

    def undo(self):
        if not self.undo_stack:
            return False
        before, after = self.undo_stack.pop()
        self.redo_stack.append((before, after))
        self.text, self.cursor = before
        self.sel = None
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        before, after = self.redo_stack.pop()
        self.undo_stack.append((before, after))
        self.text, self.cursor = after
        self.sel = None
        return True

    def select(self, a, b):
        n = len(self.text)
        a, b = sorted((max(0, min(n, a)), max(0, min(n, b))))
        self.sel = (a, b) if a < b else None

    def selected(self):
        return self.text[self.sel[0]:self.sel[1]] if self.sel else ""
