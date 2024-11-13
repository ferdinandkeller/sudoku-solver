"""
This module main function can solve a Sudoku puzzle. It uses the Z3 theorem prover to find a solution if one exists.

It also has some helper function for printing the board.
"""

from z3 import Solver, Int, And, Distinct, sat
from termcolor import colored

type Board = list[list[int]]

def solve_sudoku(board: Board | None) -> Board | None:
    """
    Tries to solve a given 9x9 Sudoku puzzle using the Z3 theorem prover.
    :param board:
        A 9x9 list representing the Sudoku board,
        where 0s indicate empty cells and integers
        from 1 to 9 represent pre-filled numbers.
    :return:
        A solved board if a solution exists, None otherwise.
    """
    if board is None:
        return None

    # Create a solver instance
    s = Solver()

    # Define the grid of integer variables
    cells = [[Int(f"x_{i}_{j}") for j in range(9)] for i in range(9)]

    # Add constraints that each cell contains an integer between 1 and n
    for i in range(9):
        for j in range(9):
            s.add(And(cells[i][j] >= 1, cells[i][j] <= 9))

    # Add constraints that each row contains all integers from 1 to n without repetition
    for i in range(9):
        s.add(Distinct([cells[i][j] for j in range(9)]))

    # Add constraints that each column contains all integers from 1 to n without repetition
    for j in range(9):
        s.add(Distinct([cells[i][j] for i in range(9)]))

    # Add constraints that each sub-grid contains all integers from 1 to n without repetition
    for ii in range(0, 9, 3):
        for jj in range(0, 9, 3):
            s.add(Distinct([cells[i][j] for i in range(ii, ii + 3) for j in range(jj, jj + 3)]))

    # Add constraints for the given numbers
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                s.add(cells[i][j] == board[i][j])

    # Check if the constraints are satisfiable
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(cells[i][j]).as_long() for j in range(9)] for i in range(9)]
        return r
    else:
        return None

def str_to_board(board_str: str) -> Board:
    """
    Parse a string representation of a Sudoku board into a 2D list.
    :param board_str: The string representation of the Sudoku board.
    :return: A 2D list representing the Sudoku board.
    """
    lines = board_str.strip().split('\n')
    lines.pop(3)
    lines.pop(6) # should be 7 but goes to 6 after row 3 is popped

    board_array = []

    for line in lines:
        elements = [elem for elem in line.split(' ') if elem]
        row = [int(elem) if elem != '.' else 0 for elem in elements]
        board_array.append(row)

    return board_array

def board_to_str(board: Board | None, compare: Board | None = None) -> str | None:
    """
    Convert a 2D list representing a Sudoku board into a string representation.
    :param board: The Sudoku board.
    :return: None
    """
    if board is None:
        return None
    out = ""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            out += "\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                out += "  "
            c = str(board[i][j])
            if compare is not None:
                if board[i][j] != compare[i][j]:
                    c = colored(c, attrs=["dark"])
            if c == "0":
                c = colored(".", attrs=["dark"])
            out += c + " "
        if i < 8:
            out += "\n"
    return out
