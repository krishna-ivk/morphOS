"""Entry point for the Sudoku GUI game.

Run:
  python -m sudoku.main
or:
  python sudoku/main.py
"""

from __future__ import annotations

import os
import sys
import tkinter as tk
from tkinter import ttk

# Allow running as a script (python sudoku/main.py)
if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sudoku.gui import SudokuGUI  # noqa: E402


def main() -> None:
    root = tk.Tk()
    root.title("Sudoku")

    try:
        # Looks nicer on Windows, harmless elsewhere.
        ttk.Style().theme_use("clam")
    except Exception:
        pass

    app = SudokuGUI(root, difficulty="medium")
    app.pack(padx=14, pady=14)

    root.minsize(860, 560)
    root.mainloop()


if __name__ == "__main__":
    main()
