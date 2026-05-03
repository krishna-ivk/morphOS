from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Literal

Board = list[list[int]]
Difficulty = Literal["easy", "medium", "hard"]

BOARD_SIZE = 9
BOX_SIZE = 3
DIGITS = tuple(range(1, 10))
CLUES_BY_DIFFICULTY: dict[Difficulty, int] = {
    "easy": 40,
    "medium": 32,
    "hard": 26,
}


@dataclass(frozen=True)
class Puzzle:
    initial: Board
    solution: Board
    difficulty: Difficulty


def clone_board(board: Board) -> Board:
    return [row[:] for row in board]


def find_empty(board: Board) -> tuple[int, int] | None:
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return row, col
    return None


def is_valid_move(board: Board, row: int, col: int, value: int) -> bool:
    if value not in DIGITS:
        return False
    for idx in range(BOARD_SIZE):
        if idx != col and board[row][idx] == value:
            return False
        if idx != row and board[idx][col] == value:
            return False

    box_row = (row // BOX_SIZE) * BOX_SIZE
    box_col = (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row, box_row + BOX_SIZE):
        for c in range(box_col, box_col + BOX_SIZE):
            if (r, c) != (row, col) and board[r][c] == value:
                return False
    return True


def board_is_complete(board: Board) -> bool:
    return all(
        value != 0 and is_valid_move(board, row, col, value)
        for row, line in enumerate(board)
        for col, value in enumerate(line)
    )


def solve_board(board: Board, rng: random.Random | None = None) -> bool:
    empty = find_empty(board)
    if empty is None:
        return True

    row, col = empty
    choices = list(DIGITS)
    if rng is not None:
        rng.shuffle(choices)

    for value in choices:
        if not is_valid_move(board, row, col, value):
            continue
        board[row][col] = value
        if solve_board(board, rng=rng):
            return True
        board[row][col] = 0
    return False


def count_solutions(board: Board, limit: int = 2) -> int:
    solutions = 0

    def _search() -> None:
        nonlocal solutions
        if solutions >= limit:
            return
        empty = find_empty(board)
        if empty is None:
            solutions += 1
            return
        row, col = empty
        for value in DIGITS:
            if not is_valid_move(board, row, col, value):
                continue
            board[row][col] = value
            _search()
            board[row][col] = 0
            if solutions >= limit:
                return

    _search()
    return solutions


def generate_full_board(rng: random.Random | None = None) -> Board:
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    generator = rng or random.Random()
    solve_board(board, rng=generator)
    return board


def generate_puzzle(
    difficulty: Difficulty = "medium", rng: random.Random | None = None
) -> Puzzle:
    generator = rng or random.Random()
    target_clues = CLUES_BY_DIFFICULTY[difficulty]
    best_puzzle: Puzzle | None = None
    best_clues = BOARD_SIZE * BOARD_SIZE + 1

    for _ in range(100):
        solution = generate_full_board(generator)
        puzzle = clone_board(solution)
        positions = [
            (row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)
        ]
        generator.shuffle(positions)
        clues_remaining = BOARD_SIZE * BOARD_SIZE

        for row, col in positions:
            if clues_remaining <= target_clues:
                break
            original = puzzle[row][col]
            puzzle[row][col] = 0
            if count_solutions(clone_board(puzzle), limit=2) != 1:
                puzzle[row][col] = original
                continue
            clues_remaining -= 1

        candidate = Puzzle(initial=puzzle, solution=solution, difficulty=difficulty)
        if clues_remaining == target_clues:
            return candidate
        if clues_remaining < best_clues:
            best_puzzle = candidate
            best_clues = clues_remaining

    if best_puzzle is None:
        raise RuntimeError("Sudoku puzzle generation failed.")
    return best_puzzle


def candidates(board: Board, row: int, col: int) -> list[int]:
    if board[row][col] != 0:
        return []
    return [value for value in DIGITS if is_valid_move(board, row, col, value)]
