from skyforce.sudoku.engine import (
    CLUES_BY_DIFFICULTY,
    board_is_complete,
    clone_board,
    count_solutions,
    generate_full_board,
    generate_puzzle,
    solve_board,
)


def test_solve_board_completes_known_puzzle():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert solve_board(puzzle) is True
    assert board_is_complete(puzzle) is True


def test_generate_full_board_creates_valid_solution():
    board = generate_full_board()
    assert board_is_complete(board) is True
    for row in board:
        assert sorted(row) == list(range(1, 10))


def test_generate_puzzle_has_unique_solution_and_target_clues():
    puzzle = generate_puzzle("medium")
    clue_count = sum(1 for row in puzzle.initial for value in row if value != 0)
    assert clue_count == CLUES_BY_DIFFICULTY["medium"]
    assert count_solutions(clone_board(puzzle.initial), limit=2) == 1
    solved = clone_board(puzzle.initial)
    assert solve_board(solved) is True
    assert solved == puzzle.solution
