# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy
import math

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here

        # initialisation of data structures
        possible_values = []
        current_values_row = []
        current_values_col = []
        current_values_square = []
        for i in range(9):
            possible_values.append([[] for j in range(9)])
            current_values_row.append(set())
            current_values_col.append(set())
        for i in range(3):
            current_values_square.append([set(), set(), set()])

        # populating of data
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    val = puzzle[i][j]
                    possible_values[i][j] = [val]
                    current_values_row[i].add(val)
                    current_values_col[j].add(val)
                    current_values_square[int(i/3)][int(j/3)].add(val)

                else:
                    possible_values[i][j].append([1, 2, 3, 4, 5, 6, 7, 8, 9])

        # maintain AC-3 arc consistency
        # remove existing values from possible values in:
        # rows
        for i in range(9):
            for j in range(9):
                curr = possible_values[i][j]
                if self.isPreFilled(puzzle, i, j):
                    continue
                for existing_value in current_values_row[i]:
                    curr.remove(existing_value)

        # col
        for i in range(9):
            for j in range(9):
                curr = possible_values[i][j]
                if self.isPreFilled(puzzle, i, j):
                    continue
                for existing_value in current_values_col[j]:
                    curr.remove(existing_value)

        # squares
        for i in range(9):
            for j in range(9):
                curr = possible_values[i][j]
                if self.isPreFilled(puzzle, i, j):
                    continue
                for existing_value in current_values_square[math.floor(i/3)][math.floor(j/3)]:
                    curr.remove(existing_value)

        # backtracking search

        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    def isPreFilled(self, puzzle, row, col):
        if type(puzzle[row][col]) is list:
            return False
        return True

    def check_row(self, puzzle, row, current_values_row):
        comparison_set = current_values_row[row]
        curr_row = puzzle[row]
        for var in curr_row:
            if var in comparison_set:
                return False
        return True

    
    def check_col(self, puzzle, col, current_values_col):
        comparison_set = current_values_col[col]
        for i in range(9):
            var = puzzle[i][col]
            if var in comparison_set:
                return False
        return True

    # square number is the top left cell of the square
    def check_square(self, puzzle, square_row, square_col, current_values_square):
        comparison_set = current_values_square[square_row][square_col]
        for i in range(3):
            for j in range(3):
                var = puzzle[square_row + i][square_col + j]
                if var in comparison_set:
                    return False
        return True

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
