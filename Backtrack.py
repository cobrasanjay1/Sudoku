import tkinter as tk
from tkinter import messagebox
from random import sample

# Function to create a random, complete Sudoku grid
def pattern(r, c): return (3*(r % 3) + r // 3 + c) % 9
def shuffle(s): return sample(s, len(s))

# Generate a randomized Sudoku puzzle based on difficulty
def generate_sudoku(difficulty):
    base = range(3)
    rows = [g * 3 + r for g in shuffle(base) for r in shuffle(base)]
    cols = [g * 3 + c for g in shuffle(base) for c in shuffle(base)]
    nums = shuffle(range(1, 10))

    grid = [[nums[pattern(r, c)] for c in cols] for r in rows]

    if difficulty == "Easy":
        empties = 30
    elif difficulty == "Medium":
        empties = 45
    else:
        empties = 60

    squares = 81
    for p in sample(range(squares), empties):
        grid[p // 9][p % 9] = 0

    return grid

# Helper functions for solving the Sudoku
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty_location(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def solve_sudoku(board):
    empty_location = find_empty_location(board)
    if not empty_location:
        return True
    row, col = empty_location

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

# Tkinter GUI Sudoku class
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.ask_for_difficulty()

    def ask_for_difficulty(self):
        self.diff_window = tk.Toplevel(self.root)
        self.diff_window.title("Choose Difficulty")
        self.root.withdraw()

        label = tk.Label(self.diff_window, text="Choose Difficulty Level", font=("Arial", 14))
        label.pack(pady=10)

        easy_button = tk.Button(self.diff_window, text="Easy", command=lambda: self.start_game("Easy"))
        easy_button.pack(pady=5)

        medium_button = tk.Button(self.diff_window, text="Medium", command=lambda: self.start_game("Medium"))
        medium_button.pack(pady=5)

        hard_button = tk.Button(self.diff_window, text="Hard", command=lambda: self.start_game("Hard"))
        hard_button.pack(pady=5)

    def start_game(self, difficulty):
        self.diff_window.destroy()
        self.grid = generate_sudoku(difficulty)
        self.root.deiconify()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        # Add the "Validate" and "Solve" buttons
        self.validate_button = tk.Button(self.root, text="Validate", command=self.validate_solution)
        self.validate_button.grid(row=9, column=0, columnspan=4)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_board)
        self.solve_button.grid(row=9, column=5, columnspan=4)

    def create_grid(self):
        for row_block in range(3):
            for col_block in range(3):
                block_frame = tk.Frame(self.root, bd=3, relief="solid")
                block_frame.grid(row=row_block * 3, column=col_block * 3, rowspan=3, columnspan=3, padx=3, pady=3)

                for row in range(3):
                    for col in range(3):
                        global_row = row_block * 3 + row
                        global_col = col_block * 3 + col

                        entry = tk.Entry(block_frame, width=2, font=('Arial', 24), justify='center', borderwidth=1,
                                         relief='solid')

                        entry.grid(row=row, column=col, padx=1, pady=1)

                        if self.grid[global_row][global_col] != 0:
                            entry.insert(0, self.grid[global_row][global_col])
                            entry.config(state='disabled')
                        self.entries[global_row][global_col] = entry

    def validate_solution(self):
        solution = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                entry_value = self.entries[row][col].get()
                if not entry_value.isdigit() or not (1 <= int(entry_value) <= 9):
                    messagebox.showwarning("Invalid Input", "Please ensure all cells contain numbers between 1 and 9.")
                    return
                solution[row][col] = int(entry_value)

        if self.is_valid_solution(solution):
            messagebox.showinfo("Success", "You won!")
        else:
            messagebox.showwarning("Error", "Try again!")

    def solve_board(self):
        board = [[int(self.entries[r][c].get()) if self.entries[r][c].get().isdigit() else 0 for c in range(9)] for r in range(9)]
        if solve_sudoku(board):
            for r in range(9):
                for c in range(9):
                    if self.grid[r][c] == 0:  # Fill only the empty cells
                        self.entries[r][c].delete(0, tk.END)
                        self.entries[r][c].insert(0, board[r][c])
        else:
            messagebox.showwarning("Error", "No solution exists for this Sudoku puzzle.")

    def is_valid_solution(self, solution):
        def is_valid_block(block):
            block = [num for num in block if num != 0]
            return len(block) == len(set(block))

        for i in range(9):
            if not is_valid_block(solution[i]) or not is_valid_block([solution[r][i] for r in range(9)]):
                return False

        for row_block in range(3):
            for col_block in range(3):
                block = [solution[r][c] for r in range(row_block * 3, (row_block + 1) * 3)
                         for c in range(col_block * 3, (col_block + 1) * 3)]
                if not is_valid_block(block):
                    return False

        return True

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    game = SudokuGUI(root)
    root.mainloop()
