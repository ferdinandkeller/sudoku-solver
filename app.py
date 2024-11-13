"""
Entrypoint of the program.
"""

from termcolor import colored
from solver import str_to_board, board_to_str, solve_sudoku

STR_BOARD = """
. . .   . . .   . . .
. . .   . . .   . 7 2
. . .   . 7 2   6 . .

. . 8   . . .   . . .
. . .   . . 6   . . 3
. . 9   . 2 3   7 . 1

. 3 .   . . .   . . .
. 1 .   . . 7   2 6 4
. 7 2   9 4 .   . 8 .
"""

board = str_to_board(STR_BOARD)
solution = board_to_str(solve_sudoku(board), board)
if solution:
    print(colored("--- sudoku solved ---", "green"))
    print(solution)
else:
    print(colored("no solution found", "red"))
