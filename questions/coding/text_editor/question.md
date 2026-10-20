---
title: Text editor with undo
difficulty: hard
category: coding
tags: design, stacks, command pattern
---
Build the editing core behind the support notes box.

## Part 1: Cursor editing

Implement `Editor()` holding `text` (starts `""`) and `cursor` (index between characters, starts 0):

- `type(s)` inserts `s` at the cursor and moves the cursor after it.
- `backspace(n=1)` deletes up to `n` characters before the cursor.
- `delete(n=1)` deletes up to `n` characters after the cursor.
- `move(k)` moves the cursor by `k` (negative is left), clamped to the text.
- `home()` / `end()` jump to the start or end.

## Part 2: Undo and redo

Add `undo()` and `redo()`, each returning `True` if something happened. Every `type`, `backspace` and `delete`
that actually changed the text is one undo step (cursor moves are not steps, and a no-op backspace at position 0 is not a step).
Undo restores the text **and** the cursor to exactly what they were before that step; redo re-applies it and restores the
cursor to where it was after. Any new edit clears the redo history.

## Part 3: Selections

Add `select(a, b)` selecting the half open range between indices `a` and `b` (any order, clamped). While a selection exists,
`type`, `backspace` and `delete` first remove the selected text (as part of the same undo step), the cursor goes to the start
of the selection, and the selection is cleared. `move`, `home`, `end` clear the selection. `selected()` returns the selected text or `""`.
