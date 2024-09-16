import tkinter as tk
from tkinter import messagebox
from random import sample

# Function to create a random, complete Sudoku grid
def pattern(r, c): return (3 * (r % 3) + r // 3 + c) % 9
def shuffle(s): return sample(s, len(s))

# Generate a randomized Sudoku puzzle based on difficulty
def generate_sudoku(difficulty):
    base = range(3)
    rows = [g * 3 + r for g in shuffle(base) for r in shuffle(base)]
    cols = [g * 3 + c for g in shuffle(base) for c in shuffle(base)]
    nums = shuffle(range(1, 10))

    # Produce a fully solved Sudoku grid
    grid = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Difficulty level empties
    if difficulty == "Easy":
        empties = 30  # Fewer empty cells
    elif difficulty == "Medium":
        empties = 45  # Moderate empty cells
    else:  # Hard
        empties = 60  # More empty cells

    # Remove random elements to create the puzzle
    squares = 81
    for p in sample(range(squares), empties):
        grid[p // 9][p % 9] = 0

    return grid

# Brute-force solver for Sudoku
def is_valid(board, row, col, num):
    # Check if 'num' is not in the current row, column, and 3x3 grid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    # Try to find an empty spot
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Empty cell found
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False  # No valid number found
    return True  # Puzzle solved

# Tkinter GUI Sudoku class
class SudokuGUI:
    def __init__(self, root):
        self.root = root

        # Ask user for difficulty level via buttons before showing the game window
        self.ask_for_difficulty()

    def ask_for_difficulty(self):
        # Create a new window for difficulty selection
        self.diff_window = tk.Toplevel(self.root)
        self.diff_window.title("Choose Difficulty")
        self.root.withdraw()  # Hide the main root window initially

        # Add label
        label = tk.Label(self.diff_window, text="Choose Difficulty Level", font=("Arial", 14))
        label.pack(pady=10)

        # Create buttons for "Easy", "Medium", and "Hard"
        easy_button = tk.Button(self.diff_window, text="Easy", command=lambda: self.start_game("Easy"))
        easy_button.pack(pady=5)

        medium_button = tk.Button(self.diff_window, text="Medium", command=lambda: self.start_game("Medium"))
        medium_button.pack(pady=5)

        hard_button = tk.Button(self.diff_window, text="Hard", command=lambda: self.start_game("Hard"))
        hard_button.pack(pady=5)

    def start_game(self, difficulty):
        # Close difficulty window
        self.diff_window.destroy()

        # Generate a random Sudoku puzzle based on difficulty
        self.grid = generate_sudoku(difficulty)

        # Now, show the main Sudoku game window
        self.root.deiconify()

        # Create a 9x9 grid of entry boxes
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        # Button to validate the user's solution
        self.validate_button = tk.Button(self.root, text="Validate", command=self.validate_solution)
        self.validate_button.grid(row=9, column=0, columnspan=4)

        # Button for brute-force solving
        self.solve_button = tk.Button(self.root, text="Bruteforce Solve", command=self.bruteforce_solution)
        self.solve_button.grid(row=9, column=5, columnspan=4)

    def create_grid(self):
        for row_block in range(3):
            for col_block in range(3):
                # Create a frame for each 3x3 block to hold the entry widgets
                block_frame = tk.Frame(self.root, bd=3, relief="solid")
                block_frame.grid(row=row_block * 3, column=col_block * 3, rowspan=3, columnspan=3, padx=3, pady=3)

                for row in range(3):
                    for col in range(3):
                        global_row = row_block * 3 + row
                        global_col = col_block * 3 + col

                        entry = tk.Entry(block_frame, width=2, font=('Arial', 24), justify='center', borderwidth=1,
                                         relief='solid')

                        # Place each entry inside the 3x3 block frame
                        entry.grid(row=row, column=col, padx=1, pady=1)

                        if self.grid[global_row][global_col] != 0:
                            entry.insert(0, self.grid[global_row][global_col])
                            entry.config(state='disabled')  # Disable pre-filled cells
                        self.entries[global_row][global_col] = entry

    def validate_solution(self):
        # Extract the grid from the entries
        solution = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.entries[row][col].get():
                    solution[row][col] = int(self.entries[row][col].get())

        # Check if the solution is valid
        if self.is_valid_solution(solution):
            messagebox.showinfo("Success", "You won!")
        else:
            messagebox.showwarning("Error", "Try again!")

    def is_valid_solution(self, solution):
        # Check rows, columns, and 3x3 grids for duplicates
        def is_valid_block(block):
            block = [num for num in block if num != 0]
            return len(block) == len(set(block))

        # Check rows and columns
        for i in range(9):
            if not is_valid_block(solution[i]) or not is_valid_block([solution[r][i] for r in range(9)]):
                return False

        # Check 3x3 subgrids
        for row_block in range(3):
            for col_block in range(3):
                block = [solution[r][c] for r in range(row_block * 3, (row_block + 1) * 3)
                         for c in range(col_block * 3, (col_block + 1) * 3)]
                if not is_valid_block(block):
                    return False

        return True

    def bruteforce_solution(self):
        # Get the current board from the entries
        board = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.entries[row][col].get():
                    board[row][col] = int(self.entries[row][col].get())

        # Solve the board using brute-force solver
        if solve_sudoku(board):
            # If solved, update the entries
            for row in range(9):
                for col in range(9):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, board[row][col])
                    self.entries[row][col].config(state='disabled')
            messagebox.showinfo("Success", "Sudoku solved using brute force!")
        else:
            messagebox.showwarning("Error", "No solution exists.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window initially
    game = SudokuGUI(root)
    root.mainloop()
