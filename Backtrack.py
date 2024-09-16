def is_valid(board, row, col, num):
    # Check if 'num' is not in the current row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check if 'num' is not in the current column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if 'num' is not in the current 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def find_empty_location(board):
    # Find the next empty cell in the grid (represented by 0)
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def solve_sudoku(board):
    # Use backtracking to solve the puzzle
    empty_location = find_empty_location(board)
    if not empty_location:
        return True  # Puzzle is solved

    row, col = empty_location

    # Try placing digits from 1 to 9 in the empty cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # Place the number and attempt to solve the rest of the puzzle
            board[row][col] = num

            if solve_sudoku(board):
                return True

            # If placing the current number doesn't lead to a solution, backtrack
            board[row][col] = 0

    return False


def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


if __name__ == "__main__":
    # Example Sudoku puzzle (0 represents empty cells)
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Sudoku Puzzle:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\nSolved Sudoku:")
        print_board(sudoku_board)
    else:
        print("No solution exists.")
