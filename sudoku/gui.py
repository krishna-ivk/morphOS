"""Tkinter GUI for Sudoku."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .sudoku import Puzzle, copy_grid, generate_puzzle, is_consistent


class SudokuGUI(ttk.Frame):
    def __init__(self, master: tk.Tk, difficulty: str = "medium"):
        super().__init__(master)
        self.master = master
        self.difficulty = difficulty

        self.puzzle_obj: Puzzle | None = None
        self.grid = [[0] * 9 for _ in range(9)]
        self.givens = [[False] * 9 for _ in range(9)]
        self.solution = [[0] * 9 for _ in range(9)]

        self.selected = (0, 0)
        self.show_errors = True

        # UI sizing
        self.cell = 52
        self.pad = 16
        self.board_px = self.cell * 9
        self.canvas_w = self.board_px + self.pad * 2
        self.canvas_h = self.board_px + self.pad * 2

        self._build_widgets()
        self.new_game()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Left: board canvas
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_w,
            height=self.canvas_h,
            bg="#0f172a",  # slate-900
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="n")
        self.canvas.bind("<Button-1>", self._on_click)

        # Key bindings
        self.master.bind("<Key>", self._on_key)

        # Right: controls
        controls = ttk.Frame(self)
        controls.grid(row=0, column=1, sticky="nw", padx=(14, 0))

        title = ttk.Label(controls, text="Sudoku", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")

        # Difficulty selector
        diff_row = ttk.Frame(controls)
        diff_row.grid(row=1, column=0, sticky="w", pady=(10, 6))
        ttk.Label(diff_row, text="Difficulty:").grid(row=0, column=0, sticky="w")
        self.diff_var = tk.StringVar(value=self.difficulty)
        diff = ttk.Combobox(
            diff_row,
            width=10,
            textvariable=self.diff_var,
            values=["easy", "medium", "hard"],
            state="readonly",
        )
        diff.grid(row=0, column=1, padx=(8, 0))

        # Buttons
        btns = ttk.Frame(controls)
        btns.grid(row=2, column=0, sticky="w", pady=(6, 10))
        ttk.Button(btns, text="New Game", command=self.new_game).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="Solve", command=self.solve).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(btns, text="Clear Cell", command=self.clear_cell).grid(row=0, column=2)

        # Toggle errors
        self.err_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            controls,
            text="Show errors",
            variable=self.err_var,
            command=self._toggle_errors,
        ).grid(row=3, column=0, sticky="w")

        # Number pad (touch-friendly)
        pad = ttk.LabelFrame(controls, text="Enter")
        pad.grid(row=4, column=0, sticky="w", pady=(10, 0))

        for i in range(9):
            n = i + 1
            r, c = divmod(i, 3)
            b = ttk.Button(pad, text=str(n), command=lambda v=n: self.place_number(v), width=6)
            b.grid(row=r, column=c, padx=6, pady=6)

        ttk.Button(pad, text="0 / Erase", command=self.clear_cell, width=20).grid(
            row=3, column=0, columnspan=3, padx=6, pady=(4, 8)
        )

        # Status line
        self.status = tk.StringVar(value="")
        ttk.Label(controls, textvariable=self.status, foreground="#334155").grid(
            row=5, column=0, sticky="w", pady=(10, 0)
        )

        # Help
        help_txt = (
            "Click a cell, then type 1-9. Backspace/Delete clears.\n"
            "Move with arrow keys."
        )
        ttk.Label(controls, text=help_txt, foreground="#475569").grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )

    def _toggle_errors(self) -> None:
        self.show_errors = bool(self.err_var.get())
        self.redraw()

    def new_game(self) -> None:
        self.difficulty = self.diff_var.get() or "medium"
        self.puzzle_obj = generate_puzzle(difficulty=self.difficulty, ensure_unique=True)

        self.grid = copy_grid(self.puzzle_obj.puzzle)
        self.solution = copy_grid(self.puzzle_obj.solution)
        self.givens = [row[:] for row in self.puzzle_obj.givens]

        self.selected = (0, 0)
        self.status.set(f"New game: {self.difficulty}")
        self.redraw()

    def solve(self) -> None:
        self.grid = copy_grid(self.solution)
        self.status.set("Solved (solution shown).")
        self.redraw()

    def clear_cell(self) -> None:
        r, c = self.selected
        if self.givens[r][c]:
            return
        self.grid[r][c] = 0
        self.status.set("")
        self.redraw()

    def place_number(self, val: int) -> None:
        r, c = self.selected
        if self.givens[r][c]:
            return

        if val == 0:
            self.grid[r][c] = 0
            self.status.set("")
            self.redraw()
            return

        # Validate move
        if self.solution[r][c] != val:
            self.grid[r][c] = val
            self.status.set("Not legal for this puzzle.")
            self.redraw()
            return

        self.grid[r][c] = val
        self.status.set("")
        self.redraw()

    def _on_click(self, ev) -> None:
        x = ev.x - self.pad
        y = ev.y - self.pad
        if x < 0 or y < 0 or x >= self.board_px or y >= self.board_px:
            return
        c = int(x // self.cell)
        r = int(y // self.cell)
        self.selected = (r, c)
        self.redraw()

    def _on_key(self, ev) -> None:
        r, c = self.selected

        # Navigation
        if ev.keysym in ("Left", "Right", "Up", "Down"):
            if ev.keysym == "Left":
                c = (c - 1) % 9
            elif ev.keysym == "Right":
                c = (c + 1) % 9
            elif ev.keysym == "Up":
                r = (r - 1) % 9
            elif ev.keysym == "Down":
                r = (r + 1) % 9
            self.selected = (r, c)
            self.redraw()
            return

        # Clear
        if ev.keysym in ("BackSpace", "Delete", "0"):
            self.clear_cell()
            return

        # Numbers
        if ev.char and ev.char in "123456789":
            self.place_number(int(ev.char))

    def _cell_bbox(self, r: int, c: int):
        x0 = self.pad + c * self.cell
        y0 = self.pad + r * self.cell
        x1 = x0 + self.cell
        y1 = y0 + self.cell
        return x0, y0, x1, y1

    def redraw(self) -> None:
        self.canvas.delete("all")

        # Background board
        x0, y0 = self.pad, self.pad
        x1, y1 = self.pad + self.board_px, self.pad + self.board_px
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#0b1220", outline="")

        # Selected cell highlight + row/col highlight
        sr, sc = self.selected
        for r in range(9):
            for c in range(9):
                bx0, by0, bx1, by1 = self._cell_bbox(r, c)
                fill = None
                if (r, c) == (sr, sc):
                    fill = "#1d4ed8"  # blue-700
                elif r == sr or c == sc:
                    fill = "#0b2a5b"  # muted blue
                if fill:
                    self.canvas.create_rectangle(bx0, by0, bx1, by1, fill=fill, outline="")

        # Error detection (for visual feedback)
        errors = [[False] * 9 for _ in range(9)]
        if self.show_errors:
            # Mark any filled cell that violates Sudoku constraints.
            # We'll do this by temporarily zeroing and testing consistency.
            for r in range(9):
                for c in range(9):
                    v = self.grid[r][c]
                    if v == 0:
                        continue
                    tmp = self.grid[r][c]
                    self.grid[r][c] = 0
                    ok = is_consistent(self.grid)
                    # Put back and check whether v itself conflicts.
                    self.grid[r][c] = tmp
                    if ok:
                        # Now test whether placing v back is consistent.
                        self.grid[r][c] = 0
                        self.grid[r][c] = tmp
                        if not is_consistent(self.grid):
                            errors[r][c] = True
                    else:
                        errors[r][c] = True

        # Numbers
        done = True
        for r in range(9):
            for c in range(9):
                v = self.grid[r][c]
                if v == 0:
                    done = False
                    continue

                bx0, by0, bx1, by1 = self._cell_bbox(r, c)
                cx = (bx0 + bx1) / 2
                cy = (by0 + by1) / 2

                if self.givens[r][c]:
                    color = "#e2e8f0"  # slate-200
                    font = ("Segoe UI", 18, "bold")
                else:
                    color = "#a5b4fc"  # indigo-300
                    font = ("Segoe UI", 18, "normal")

                # Completed cell feedback
                if not self.givens[r][c] and v == self.solution[r][c]:
                    color = "#86efac"  # green-300

                # Error feedback
                if self.show_errors and not self.givens[r][c] and errors[r][c]:
                    color = "#fb7185"  # rose-400

                self.canvas.create_text(cx, cy, text=str(v), fill=color, font=font)

        # Grid lines
        for i in range(10):
            w = 3 if i % 3 == 0 else 1
            col = "#334155" if i % 3 == 0 else "#1f2937"
            # vertical
            x = self.pad + i * self.cell
            self.canvas.create_line(x, self.pad, x, self.pad + self.board_px, fill=col, width=w)
            # horizontal
            y = self.pad + i * self.cell
            self.canvas.create_line(self.pad, y, self.pad + self.board_px, y, fill=col, width=w)

        # Completion status
        if done and self.grid == self.solution:
            self.status.set("Completed! 🎉")
            # subtle overlay
            self.canvas.create_rectangle(
                self.pad,
                self.pad,
                self.pad + self.board_px,
                self.pad + self.board_px,
                fill="#10b981",
                stipple="gray25",
                outline="",
            )
            self.canvas.create_text(
                self.pad + self.board_px / 2,
                self.pad + self.board_px / 2,
                text="Completed!",
                fill="#052e16",
                font=("Segoe UI", 26, "bold"),
            )
