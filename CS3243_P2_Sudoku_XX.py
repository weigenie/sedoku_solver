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
        powers_of_two = (1, 2, 4, 8, 16, 32, 64, 128, 256)
        powers_of_two_test = [i in powers_of_two for i in range(512)]
        set_bitmask = lambda val: powers_of_two[val - 1]
        # def set_bitmask(val):
        #     print val - 1, len(powers_of_two)
        #     return powers_of_two[val - 1]
        clear_bitmask = lambda val: 511 - set_bitmask(val) # 511 = 0b111111111

        is_singleton = lambda val: powers_of_two_test[val]
        get_singleton = lambda val: int(math.log(val, 2))
        contains_value = lambda domain, val: (domain & set_bitmask(val)) != 0
        domain_size = lambda domain: sum([1 if domain & i else 0 for i in powers_of_two])

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
                            current_values_row[i] |= newVal
                            current_values_col[j] |= newVal
                            current_values_square[int(i/3)][int(j/3)] |= newVal
            
            if not changes:
                break

        # verify arc consistency (a singleton value is not repeated in any rows/cols/squares domains)
        def print_matrix(possible_values):
            for i in possible_values:
                print [bin(j) if j != 0 else "X" for j in i]
            print "\n"
        
        def goal_test(state):
            for i in range(9):
                for j in range(9):
                    if not is_singleton(state[i][j]):
                        return False
            for i in range(9):
                if sum(state[i]) != 511:
                    return False
            for j in range(9):
                if sum([i[j] for i in state]) != 511:
                    return False
            for i in range(3):
                for j in range(3):
                    s = 0
                    for x in range(3):
                        for y in range(3):
                            s += state[i*3+x][j*3+y]
                    if s != 511:
                        return False
            # return consistency_test(state)
            return True
        
        def consistency_test(state):
            # non-complete state
            for i in state:
                s = filter(is_singleton, i)
                if len(s) != len(set(s)):
                    return False
            for j in range(9):
                s = filter(is_singleton, [i[j] for i in state])
                if len(s) != len(set(s)):
                    return False
            for i in range(3):
                for j in range(3):
                    s = []
                    for x in range(3):
                        for y in range(3):
                            if is_singleton(state[i*3+x][j*3+y]):
                                s += [state[i*3+x][j*3+y]]
                    if len(s) != len(set(s)):
                        return False
            return True
                    
        
        def select_unassigned_variable(state):
            # select non-singleton variable with smallest domain
            min_size = 10
            pos = None
            for i in range(9):
                for j in range(9):
                    size = domain_size(state[i][j])
                    if size > 1:
                        if size < min_size:
                            min_size = size
                            pos = (i, j)
            return pos

        def order_domain_values(state, var):
            # greedily order 1 .. 9 if it exists in the domain
            val = state[var[0]][var[1]]
            domain = []
            for i in range(9):
                if contains_value(val, i):
                    domain += [i]
            return domain
        
        # backtracking search
        def backtrack(state):
            # print_matrix(state)
            if goal_test(state):
                return state
            to_assign = select_unassigned_variable(state)
            if to_assign is None:
                return None
            for newVal in order_domain_values(state, to_assign):
                new_state = [[state[i][j] for j in range(9)] for i in range(9)]
                # assign value newVal to variable to_assign
                i, j = to_assign
                # current_values_row[i] |= set_bitmask(newVal)
                # current_values_col[j] |= set_bitmask(newVal)
                # current_values_square[int(i/3)][int(j/3)] |= set_bitmask(newVal)

                consistent = True

                for x in range(9):
                    new_state[x][j] &= clear_bitmask(newVal)
                    if new_state[x][j] is 0:
                        consistent = False
                        break

                if consistent:
                    for y in range(9):
                        if y is j:
                            continue
                        new_state[i][y] &= clear_bitmask(newVal)
                        if new_state[i][y] is 0:
                            consistent = False
                            break

                if consistent:
                    rounded_down = (0,0,0,3,3,3,6,6,6)
                    for x in range(3):
                        for y in range(3):
                            if i % 3 is x or j % 3 is y:
                                continue
                            new_state[x+rounded_down[i]][y+rounded_down[j]] &= clear_bitmask(newVal)
                            if new_state[x+rounded_down[i]][y+rounded_down[j]] is 0:
                                consistent = False
                                break # should break outer as well
                
                new_state[i][j] = set_bitmask(newVal)

                consistent &= consistency_test(new_state)

                if not consistent:
                    continue

                step = backtrack(new_state)
                if step is not None:
                    return step

                # current_values_row[i] &= clear_bitmask(newVal)
                # current_values_col[j] &= clear_bitmask(newVal)
                # current_values_square[int(i/3)][int(j/3)] &= clear_bitmask(newVal)

            return None # failure
        
        result = backtrack(possible_values)

        # need to reduce from bitset back to numbers
        self.ans = [[get_singleton(j) + 1 for j in i] for i in result]

        for i in self.ans:
            print i

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
