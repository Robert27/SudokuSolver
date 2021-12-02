import os
from time import perf_counter
from typing import Optional


class Sudoku:
    """Sudoku Solver Class"""

    def __init__(self, path: str) -> object:
        """Initializes the grid
        :param path: Path to the grid file
        """
        self.grid = self.load_grid(path)  # Loads the grid from a file
        self.solved = False
        self.start = 0.0
        self.time = 0.0

    def solve(self) -> list[list[int]]:
        """Solves the grid using the backtracking algorithm
        :return: The solved grid
        """
        self.start = perf_counter()
        if not self.recursive_solve():
            print('Error: Grid is unsolvable')
        else:
            print('Grid solved in {} ms'.format(self.time_taken()))
        return self.grid

    def recursive_solve(self) -> bool:
        """Recursive backtracking algorithm to solve the grid
        :return: True if solved, False otherwise
        """
        result = self.find_empty_cell()
        if result:
            row, col = result
        else:
            self.time = perf_counter() - self.start
            return True

        for i in range(1, 10, 1):
            if self.check(i, (row, col)):
                self.grid[row][col] = i

                if self.recursive_solve():
                    return True  # Recursive call

                self.grid[row][col] = 0  # Backtracking
        return False  # No solution found

    def check(self, digit: int, position: tuple[int, int]) -> bool:
        """Checks if the number is valid in the row, column and region
        :param digit: Number to check
        :param position: (row, column)
        :return: True if valid, False otherwise
        """
        col, row = position
        region_row: int = (row // 3) * 3
        region_col: int = (col // 3) * 3

        for i in range(9):  # Iterate through rows and columns
            if col != i and self.grid[i][row] == digit:  # If number is in the same column
                return False
            elif row != i and self.grid[col][i] == digit:  # If number is in the same row
                return False

        # Iterate through region
        for i in range(region_col, region_col + 3):
            for j in range(region_row, region_row + 3):
                if self.grid[i][j] == digit and (i, j) != position:  # If number is in region and not the cell
                    return False

        return True

    def print_grid(self) -> None:
        """Prints the grid to the console in a readable format"""

        for i in range(9):
            row: str = ''
            for j in range(9):
                cell: int = self.grid[i][j]
                if cell == 0 or isinstance(cell, set):  # If cell is empty or a set
                    row += '⬚'
                else:
                    row += str(cell)
                if (j + 1) % 3 == 0 and j < 8:  # Adds a space after every third number
                    row += ' ┃'

                if j != 8:  # If not the last cell
                    row += ' '
            print(row)
            if (i + 1) % 3 == 0 and i < 8:  # Prints a line between 3x3 regions
                print("━━━━━━╋━━━━━━━╋━━━━━━")
        print()

    def find_empty_cell(self) -> Optional[tuple[int, int]]:
        """Finds the first empty cell in the grid and returns its coordinates
        :return: (row, column)
        """
        for i in range(9):  # Iterate through rows
            for j in range(9):  # Iterate through columns
                if self.grid[i][j] == 0:  # If cell is empty
                    return i, j

        return None  # No empty cell found

    @staticmethod
    def load_grid(path: str) -> list[list[int]]:
        """Loads the grid from a file and returns it as a list of lists
        :param path: Path to the file
        :return: List of lists
        """
        with open(path, 'r') as f:
            data = [l for l in (line.strip() for line in f) if l]  # Remove empty lines
        grid: list[list[int]] = []
        for i in data:
            if len(i) != 9 or not i.isdigit():  # If line is not 9 characters long or not a number
                raise ValueError(f'Invalid grid in row {data.index(i)}: {i}')
            numbers: list[int] = [int(x) for x in list(i)]
            grid.append(numbers)
        print(f'Loaded grid from {path}')
        return grid

    def time_taken(self) -> float:
        """Returns the time taken to solve the grid in milliseconds
        :return: Time taken in milliseconds
        """
        return round(self.time * 1000, 2)


def test_solver(path: str) -> None:
    """Tests the solver on all the grids in the given path
    :param path: Path to the folder containing the grids
    """
    files = os.listdir(path)
    times: list[float] = []
    print("Testing solver on files in sudokus folder")
    for f in files:
        print(f'Testing {f}')
        solver: Sudoku = Sudoku(path='sudokus_test/' + f)
        solver.solve()
        times.append(solver.time_taken())
        print()
    average_time: float = round(sum(times) / len(times), 2)
    print(f'Average time: {average_time} ms')


if __name__ == "__main__":
    solver: Sudoku = Sudoku(path='sudokus_test/sudoku04.txt')
    solver.print_grid()  # Prints the grid before solving
    solver.solve()
    solver.print_grid()  # Prints the grid after solving

    # Test the solver on all files in the sudokus_test folder
    test_solver(path='sudokus_test')
