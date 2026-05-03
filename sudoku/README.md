# Sudoku (Tkinter)

A complete Sudoku puzzle game with a graphical UI.

## Features

- 9x9 grid with **pre-filled numbers** and empty cells
- Mouse/touch-friendly cell selection and number pad (1–9 + erase)
- Move validation (only accepts numbers that match the puzzle’s solution)
- **New Game** button (generates a different puzzle)
- **Solve** button (shows the solution)
- Visual feedback:
  - wrong entries highlighted **red**
  - correct user-filled entries highlighted **green**
  - completion overlay when solved

## Run

From the repo root:

```bash
python -m sudoku.main
```

Or:

```bash
python sudoku/main.py
```

## Notes

- Uses only the Python standard library (Tkinter).
- Puzzle generation uses a random solved grid + clue removal, with an optional uniqueness check (enabled by default).
