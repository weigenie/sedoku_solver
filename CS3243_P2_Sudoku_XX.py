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
        possible_values = [[0 for j in range(9)] for i in range(9)]
        current_values_row = [0 for i in range(9)]
        current_values_col = [0 for j in range(9)]
        current_values_square = [[0 for j in range(3)] for i in range(3)]

        # helper functions for bitwise operations
        set_bitmask = lambda val: 1 << (val - 1)
        clear_bitmask = lambda val: 511 - set_bitmask(val) # 511 = 0b111111111

        powers_of_two = [i in (1, 2, 4, 8, 16, 32, 64, 128, 256) for i in range(512)]
        is_singleton = lambda val: powers_of_two[val]
        get_singleton = lambda val: int(math.log(val, 2))

        # populating of data
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    val = set_bitmask(puzzle[i][j])
                    possible_values[i][j] = val
                    current_values_row[i] |= val
                    current_values_col[j] |= val
                    current_values_square[int(i/3)][int(j/3)] |= val
                else:
                    possible_values[i][j] = 511

        # maintain AC-3 arc consistency
        # remove existing values from possible values in:

        while True:
            # Can be optimized to AC-3 later.
            # Wikipedia:
            # A simplistic algorithm would cycle over the pairs of variables, enforcing arc-consistency,
            # repeating the cycle until no domains change for a whole cycle.
            changes = False

            # rows, cols, squares
            for i in range(9):
                for j in range(9):
                    if is_singleton(possible_values[i][j]):
                        continue # fixed, do nothing as it is already represented in current_values
                    # restrict newVal based on the current_values
                    newVal = possible_values[i][j] & ~current_values_row[i] & ~current_values_col[j] & ~current_values_square[int(i/3)][int(j/3)]
                    # if it changes, set a flag to iterate again
                    if newVal != possible_values[i][j]:
                        changes = True
                        possible_values[i][j] = newVal
                        # if this is a singleton, add it to the current_values
                        if is_singleton(newVal):
                            current_values_row[i] |= set_bitmask(newVal)
                            current_values_col[j] |= set_bitmask(newVal)
                            current_values_square[int(i/3)][int(j/3)] |= set_bitmask(newVal)
            
            if not changes:
                break

        # verify arc consistency (a singleton value is not repeated in any rows/cols/squares domains)
        for i in possible_values:
            print [bin(j) for j in i]
        
        def goal_test(possible_values):
            for i in range(9):
                for j in range(9):
                    if not is_singleton(possible_values[i][j])
                        return False
            return True
        
        # backtracking search

        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    def isPreFilled(self, puzzle, row, col):
        return puzzle[row][col] != 0

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
