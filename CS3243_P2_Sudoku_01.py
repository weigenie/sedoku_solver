# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy
import math

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

# constraints:
# each row only have one instance of 1..9
# each col only have one instance of 1..9
# each square only have one instance of 1..9
class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

    def solve(self):
        self.initDataStructure()

        if self.backtrack():
            return self.ans
        
        return "Sudoku cannot be solved."

    def initDataStructure(self):
        rowMissingN = [[True] * 10 for i in range(9)]
        colMissingN = [[True] * 10 for i in range(9)]
        squareMissingN = [[True] * 10 for i in range(9)]
        
        self.constraintChecks = [rowMissingN, colMissingN, squareMissingN]
        self.numAssignCount = [0] * 10
        self.unassigned = set()

        for i in range(9):
            for j in range(9):
                curr = self.ans[i][j]

                if curr != 0:
                    # print("assigning: " + str(curr))
                    self.assignInit((i, j, []), curr)
                else:
                    self.unassigned.add((i, j))
                    
    def getSquareNum(self, i, j):
        return i // 3 + (j // 3) * 3

    def backtrack(self):
        var = self.getUnassignedVariable()

        if var is None:
            return True
        elif var == False:
            return False

        var[2].sort(key = lambda x: self.numAssignCount[x])
        for num in var[2]:
            self.assign(var, num)

            if self.backtrack():
                return True

            self.unassign(var, num)

    # using the minimum remaining value heuristic
    # get the cell with the minimum domain size
    def getUnassignedVariable(self):
        minDomainSize = 99
        returnVariable = None

        for pair in self.unassigned:
            i, j = pair
            curr = self.ans[i][j]

            if curr != 0:
                continue

            domain = self.getDomain(i, j)
            domainSize = len(domain)

            if domainSize == 0:
                return False

            elif domainSize == 1:
                return (i, j, domain)

            else:
                if domainSize < minDomainSize:
                    returnVariable = (i, j, domain)
                    minDomainSize = domainSize


        return returnVariable

    def getDomain(self, i, j):
        rowMissingN = self.constraintChecks[0][i]
        colMissingN = self.constraintChecks[1][j]
        squareMissingN = self.constraintChecks[2][self.getSquareNum(i, j)]

        domain = []
        for num in range(1, 10):
            if rowMissingN[num] and colMissingN[num] and squareMissingN[num]:
                domain.append(num)
        return domain

    # using least constraining value heuristic
    # get domain in the order of least constraining to most constraining
    # least constraining value is the number that has been assigned the least
    def getSortedDomain(self, var):
        originalDomain = var[2]
        originalDomain.sort(key = lambda x: self.numAssignCount[x])
        return originalDomain

    def assign(self, var, num):
        i, j, domain = var
        rowMissingN = self.constraintChecks[0][i]
        colMissingN = self.constraintChecks[1][j]
        squareMissingN = self.constraintChecks[2][self.getSquareNum(i, j)]

        self.ans[i][j] = num
        self.unassigned.remove((i, j))
        rowMissingN[num] = False
        colMissingN[num] = False
        squareMissingN[num] = False
        self.numAssignCount[num] = self.numAssignCount[num] + 1
    
    def assignInit(self, var, num):
        # same as assign but without the self.unassigned removal
        i, j, domain = var
        rowMissingN = self.constraintChecks[0][i]
        colMissingN = self.constraintChecks[1][j]
        squareMissingN = self.constraintChecks[2][self.getSquareNum(i, j)]

        self.ans[i][j] = num
        rowMissingN[num] = False
        colMissingN[num] = False
        squareMissingN[num] = False
        self.numAssignCount[num] = self.numAssignCount[num] + 1

    def unassign(self, var, num):
        i, j, domain = var
        rowMissingN = self.constraintChecks[0][i]
        colMissingN = self.constraintChecks[1][j]
        squareMissingN = self.constraintChecks[2][self.getSquareNum(i, j)]

        self.ans[i][j] = 0
        self.unassigned.add((i, j))
        rowMissingN[num] = True
        colMissingN[num] = True
        squareMissingN[num] = True
        self.numAssignCount[num] = self.numAssignCount[num] - 1

        
        
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
            