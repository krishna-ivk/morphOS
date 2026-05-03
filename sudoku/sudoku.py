"""Sudoku game logic: generator, solver, and move validation.

No third-party deps.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional, Tuple

Grid = List[List[int]]  # 9x9, 0 means empty


def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]


def find_empty(g: Grid) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                return r, c
    return None


def is_legal(g: Grid, r: int, c: int, val: int) -> bool:
    if val < 1 or val > 9:
        return False
    # Row/col
    if any(g[r][x] == val for x in range(9)):
        return False
    if any(g[x][c] == val for x in range(9)):
        return False
    # Box
    br = (r // 3) * 3
    bc = (c // 3) * 3
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            if g[rr][cc] == val:
                return False
    return True


def solve_inplace(g: Grid) -> bool:
    """Backtracking solver. Mutates g. Returns True if solved."""
    empty = find_empty(g)
    if empty is None:
        return True
    r, c = empty

    nums = list(range(1, 10))
    random.shuffle(nums)
    for val in nums:
        if is_legal(g, r, c, val):
            g[r][c] = val
            if solve_inplace(g):
                return True
            g[r][c] = 0
    return False


def count_solutions(g: Grid, limit: int = 2) -> int:
    """Count solutions up to `limit` (for uniqueness testing)."""
    empty = find_empty(g)
    if empty is None:
        return 1
    r, c = empty

    total = 0
    for val in range(1, 10):
        if is_legal(g, r, c, val):
            g[r][c] = val
            total += count_solutions(g, limit=limit)
            g[r][c] = 0
            if total >= limit:
                return total
    return total


def generate_full_solution(seed: Optional[int] = None) -> Grid:
    if seed is not None:
        random.seed(seed)
    g: Grid = [[0] * 9 for _ in range(9)]
    ok = solve_inplace(g)
    if not ok:
        # Extremely unlikely with this approach, but be safe.
        raise RuntimeError("Failed to generate a solved Sudoku grid")
    return g


@dataclass(frozen=True)
class Puzzle:
    puzzle: Grid
    solution: Grid
    givens: List[List[bool]]


def generate_puzzle(
    difficulty: str = "medium",
    ensure_unique: bool = True,
    seed: Optional[int] = None,
) -> Puzzle:
    """Generate a Sudoku puzzle.

    difficulty: easy|medium|hard

    Notes:
    - We generate a random full solution and then remove numbers.
    - If ensure_unique=True, we keep removals only when the puzzle still
      has a unique solution (checked with a capped solver).

    This is not the fastest generator, but it's fine for a GUI game.
    """

    if seed is not None:
        random.seed(seed)

    solution = generate_full_solution()
    puzzle = copy_grid(solution)

    # How many clues to keep (roughly). Lower clues => harder.
    # Typical ranges: easy 36-45, medium 30-36, hard 22-30.
    clues_map = {
        "easy": 40,
        "medium": 34,
        "hard": 28,
    }
    clues = clues_map.get(difficulty, 34)
    removals_target = 81 - clues

    coords = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(coords)

    removed = 0
    for (r, c) in coords:
        if removed >= removals_target:
            break

        if puzzle[r][c] == 0:
            continue

        backup = puzzle[r][c]
        puzzle[r][c] = 0

        if ensure_unique:
            test = copy_grid(puzzle)
            nsol = count_solutions(test, limit=2)
            if nsol != 1:
                puzzle[r][c] = backup
                continue

        removed += 1

    givens = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
    return Puzzle(puzzle=puzzle, solution=solution, givens=givens)


def is_complete(g: Grid) -> bool:
    return all(g[r][c] != 0 for r in range(9) for c in range(9))


def is_consistent(g: Grid) -> bool:
    """Check if the current grid violates Sudoku constraints (ignoring zeros)."""
    # Rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = g[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # Cols
    for c in range(9):
        seen = set()
        for r in range(9):
            v = g[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # Boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = g[r][c]
                    if v == 0:
                        continue
                    if v in seen:
                        return False
                    seen.add(v)
    return True
