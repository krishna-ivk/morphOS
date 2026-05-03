from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from .engine import (
    Board,
    Puzzle,
    board_is_complete,
    clone_board,
    generate_puzzle,
    is_valid_move,
)


class SudokuApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)

        self.difficulty_var = tk.StringVar(value="medium")
        self.status_var = tk.StringVar(value="Create a new game to start.")
        self.timer_var = tk.StringVar(value="Time: 00:00")
        self.seed_value = random.randrange(1_000_000)

        self.entries: list[list[tk.Entry]] = []
        self.entry_vars: list[list[tk.StringVar]] = []
        self.givens: set[tuple[int, int]] = set()
        self.puzzle: Puzzle | None = None
        self.board: Board = [[0 for _ in range(9)] for _ in range(9)]
        self.start_time = time.monotonic()
        self.timer_job: str | None = None

        self._build_ui()
        self.new_game()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        controls = ttk.Frame(frame)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(controls, text="Difficulty").grid(row=0, column=0, padx=(0, 8))
        difficulty = ttk.Combobox(
            controls,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10,
        )
        difficulty.grid(row=0, column=1, padx=(0, 12))

        ttk.Button(controls, text="New Game", command=self.new_game).grid(
            row=0, column=2, padx=4
        )
        ttk.Button(controls, text="Reset", command=self.reset_board).grid(
            row=0, column=3, padx=4
        )
        ttk.Button(controls, text="Hint", command=self.show_hint).grid(
            row=0, column=4, padx=4
        )
        ttk.Button(controls, text="Check", command=self.check_progress).grid(
            row=0, column=5, padx=4
        )
        ttk.Button(controls, text="Solve", command=self.solve_puzzle).grid(
            row=0, column=6, padx=4
        )

        board_frame = ttk.Frame(frame, padding=4)
        board_frame.grid(row=1, column=0, sticky="nsew")

        for box_row in range(3):
            for box_col in range(3):
                subframe = tk.Frame(
                    board_frame,
                    bg="#202020",
                    highlightbackground="#202020",
                    highlightthickness=1,
                    padx=1,
                    pady=1,
                )
                subframe.grid(row=box_row, column=box_col, padx=2, pady=2)
                for inner_row in range(3):
                    for inner_col in range(3):
                        row = box_row * 3 + inner_row
                        col = box_col * 3 + inner_col
                        variable = tk.StringVar()
                        entry = tk.Entry(
                            subframe,
                            width=2,
                            justify="center",
                            font=("Helvetica", 20, "bold"),
                            textvariable=variable,
                            relief="flat",
                            bd=0,
                            highlightthickness=1,
                        )
                        entry.grid(row=inner_row, column=inner_col, padx=1, pady=1)
                        entry.bind("<KeyRelease>", self._on_key_release)
                        entry.bind(
                            "<FocusIn>",
                            lambda event, r=row, c=col: self._highlight_focus(r, c),
                        )
                        entry.bind(
                            "<Up>", lambda event, r=row, c=col: self._move_focus(r - 1, c)
                        )
                        entry.bind(
                            "<Down>",
                            lambda event, r=row, c=col: self._move_focus(r + 1, c),
                        )
                        entry.bind(
                            "<Left>",
                            lambda event, r=row, c=col: self._move_focus(r, c - 1),
                        )
                        entry.bind(
                            "<Right>",
                            lambda event, r=row, c=col: self._move_focus(r, c + 1),
                        )
                        if len(self.entries) <= row:
                            self.entries.append([])
                            self.entry_vars.append([])
                        self.entries[row].append(entry)
                        self.entry_vars[row].append(variable)

        sidebar = ttk.Frame(frame, padding=(16, 4, 0, 4))
        sidebar.grid(row=1, column=1, sticky="ns")
        ttk.Label(sidebar, textvariable=self.timer_var, font=("Helvetica", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        ttk.Label(
            sidebar,
            text="Rules:\nFill every row, column,\nand 3x3 box with 1-9.",
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))
        ttk.Label(
            sidebar,
            text="Hint fills one cell.\nCheck highlights mistakes.\nSolve reveals the board.",
            justify="left",
        ).grid(row=2, column=0, sticky="w")

        ttk.Label(
            frame,
            textvariable=self.status_var,
            wraplength=560,
            justify="left",
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def new_game(self) -> None:
        difficulty = self.difficulty_var.get()
        rng = random.Random(self.seed_value)
        self.seed_value += 1
        self.puzzle = generate_puzzle(difficulty=difficulty, rng=rng)
        self.board = clone_board(self.puzzle.initial)
        self.givens = {
            (row, col)
            for row in range(9)
            for col in range(9)
            if self.puzzle and self.puzzle.initial[row][col] != 0
        }
        self.start_time = time.monotonic()
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self._render_board()
        self._update_timer()
        self.status_var.set(f"New {difficulty} puzzle ready.")

    def reset_board(self) -> None:
        if self.puzzle is None:
            return
        self.board = clone_board(self.puzzle.initial)
        self._render_board()
        self.status_var.set("Board reset to the starting puzzle.")

    def solve_puzzle(self) -> None:
        if self.puzzle is None:
            return
        self.board = clone_board(self.puzzle.solution)
        self._render_board()
        self.status_var.set("Puzzle solved.")

    def show_hint(self) -> None:
        if self.puzzle is None:
            return
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != self.puzzle.solution[row][col]:
                    self.board[row][col] = self.puzzle.solution[row][col]
                    self._render_board()
                    self.status_var.set(
                        f"Hint: row {row + 1}, column {col + 1} was filled."
                    )
                    return
        self.status_var.set("No hint needed. The board is already solved.")

    def check_progress(self) -> None:
        if self.puzzle is None:
            return
        mistakes = []
        empties = 0
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value == 0:
                    empties += 1
                    continue
                if value != self.puzzle.solution[row][col]:
                    mistakes.append((row, col))
        self._refresh_colors(mistakes=mistakes)
        if mistakes:
            self.status_var.set(f"{len(mistakes)} incorrect cell(s) highlighted.")
        elif empties:
            self.status_var.set("No mistakes found so far.")
        else:
            self.status_var.set("Board complete.")
            messagebox.showinfo("Sudoku", "You solved the puzzle.")

    def _render_board(self) -> None:
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                variable = self.entry_vars[row][col]
                entry = self.entries[row][col]
                variable.set("" if value == 0 else str(value))
                if (row, col) in self.givens:
                    entry.configure(
                        state="readonly",
                        readonlybackground="#e7eef7",
                        fg="#1d3557",
                        disabledforeground="#1d3557",
                    )
                else:
                    entry.configure(state="normal", bg="white", fg="#111111")
        self._refresh_colors()

    def _update_timer(self) -> None:
        elapsed = int(time.monotonic() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)
        self.timer_var.set(f"Time: {minutes:02d}:{seconds:02d}")
        self.timer_job = self.root.after(1000, self._update_timer)

    def _move_focus(self, row: int, col: int) -> str:
        row = max(0, min(8, row))
        col = max(0, min(8, col))
        self.entries[row][col].focus_set()
        return "break"

    def _highlight_focus(self, row: int, col: int) -> None:
        self._refresh_colors(active=(row, col))

    def _on_key_release(self, event: tk.Event) -> None:
        widget = event.widget
        row, col = self._locate_entry(widget)
        if (row, col) in self.givens:
            return

        text = self.entry_vars[row][col].get().strip()
        filtered = text[-1] if text and text[-1] in "123456789" else ""
        self.entry_vars[row][col].set(filtered)
        self.board[row][col] = int(filtered) if filtered else 0

        self._refresh_colors(active=(row, col))
        if board_is_complete(self.board):
            self.status_var.set("Board complete.")
            messagebox.showinfo("Sudoku", "You solved the puzzle.")
            return

        if filtered:
            if is_valid_move(self.board, row, col, int(filtered)):
                self.status_var.set("Entry accepted.")
            else:
                self.status_var.set("That entry conflicts with the board.")
        else:
            self.status_var.set("Cell cleared.")

    def _refresh_colors(
        self,
        active: tuple[int, int] | None = None,
        mistakes: list[tuple[int, int]] | None = None,
    ) -> None:
        mistake_set = set(mistakes or [])
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                value = self.board[row][col]
                given = (row, col) in self.givens
                same_box = (
                    active is not None
                    and row // 3 == active[0] // 3
                    and col // 3 == active[1] // 3
                )
                same_line = active is not None and (
                    row == active[0] or col == active[1]
                )
                bg = "#ffffff"
                if given:
                    bg = "#e7eef7"
                if same_box or same_line:
                    bg = "#f8f1d7" if not given else "#dde8f5"
                if active == (row, col):
                    bg = "#ffe29a"

                fg = "#111111"
                if given:
                    fg = "#1d3557"
                if value and not is_valid_move(self.board, row, col, value):
                    fg = "#c1121f"
                if (row, col) in mistake_set:
                    bg = "#ffd6d6"
                    fg = "#9d0208"

                if given:
                    entry.configure(readonlybackground=bg, fg=fg, disabledforeground=fg)
                else:
                    entry.configure(bg=bg, fg=fg)

    def _locate_entry(self, widget: object) -> tuple[int, int]:
        for row, line in enumerate(self.entries):
            for col, entry in enumerate(line):
                if entry is widget:
                    return row, col
        raise ValueError("Entry widget is not registered.")


def launch() -> None:
    root = tk.Tk()
    SudokuApp(root)
    root.mainloop()
