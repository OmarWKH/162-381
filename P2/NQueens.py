import random
import unittest
from datetime import datetime
import sys

def getRandomAssignment(n):
    '''
    col == index
    row = queens[col]
    top left is (0, 0)
    '''
    return random.sample(xrange(0, n), n)

def isSolved(queens):
    for column in range(0, len(queens)):
        if hasConflict(column, queens, True):
            return False
    return True

def hasConflict(indexOfQueen, queens, excludePrevious):
    queen = (indexOfQueen, queens[indexOfQueen])
    indexOfNext = indexOfQueen + 1 if excludePrevious else 0

    for col, row in enumerate(queens[indexOfNext:], indexOfNext):
        otherQueen = (col, row)
        if sameRow(queen, otherQueen):
            return True
        if sameDiagonal(queen, otherQueen):
            return True
    return False

def numberOfConfilct(indexOfQueen, queens, maxConflicts=sys.maxint):
    conflicts = 0
    queen = (indexOfQueen, queens[indexOfQueen])
    indexOfNext = indexOfQueen + 1

    # (R)ight, (L)eft, U(p), D(own)
    rowR = False
    rowL = False
    diagonalUR = False
    diagonalUL = False
    diagonalDR = False
    diagonalDL = False

    for col, row in enumerate(queens[indexOfNext:], indexOfNext):
        otherQueen = (col, row)
        allTrue = rowR and rowL and diagonalUR and diagonalUL and diagonalDR and diagonalDL
        if allTrue:
            break
        if conflicts > maxConflicts:
            return sys.maxint
        if not rowR:
            rowR = sameRow(queen, otherQueen) and queen[0] < otherQueen[0]
            conflicts += 1 if rowR else 0
        if not rowL:
            rowL = sameRow(queen, otherQueen) and queen[0] > otherQueen[0]
            conflicts += 1 if rowL else 0
        if not diagonalUR:
            diagonalUR = sameDiagonal(queen, otherQueen) and queen[0] < otherQueen[0] and queen[1] > otherQueen[1]
            conflicts += 1 if diagonalUR else 0
        if not diagonalDR:
            diagonalDR = sameDiagonal(queen, otherQueen) and queen[0] < otherQueen[0] and  queen[1] < otherQueen[1]
            conflicts += 1 if diagonalDR else 0
        if not diagonalUL:
            diagonalUL = sameDiagonal(queen, otherQueen) and queen[0] > otherQueen[0] and queen[1] > otherQueen[1]
            conflicts += 1 if diagonalUL else 0
        if not diagonalDL:
            diagonalDL = sameDiagonal(queen, otherQueen) and queen[0] > otherQueen[0] and queen[1] < otherQueen[1]
            conflicts += 1 if diagonalDL else 0
    return conflicts

def sameRow(queen1, queen2):
    return queen1[1] == queen2[1]

def sameDiagonal(queen1, queen2):
    return abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1])

def mutate(queens, excludeQueen=None):
    queen, altQueen = random.sample(queens, 2)
    queen = queen if queen != excludeQueen else altQueen
    row = minConflictValue(queen, queens)
    queens[queen] = row
    return (queens, queen) # mutated, variable to exclue next

def minConflictValue(queenColumn, queens):# n
    minConfilct = sys.maxint
    minRows = []
    for row in range(0, len(queens)):
        queens[queenColumn] = row
        # only check affected
        numConflicts = numberOfConfilct(queenColumn, queens, minConfilct)
        if numConflicts < minConfilct:
            minConfilct = numConflicts
            minRows = [row]
        elif numConflicts == minConfilct:
            minRows.append(row)

    return minRows[random.randrange(0, len(minRows))]

def solve(n, doDisplay, initial=None):
    startTime = datetime.now()
    random.seed()

    # not this is useless except for logging/display
    initialQueens = initial or getRandomAssignment(n)
    queens = list(initialQueens)

    if doDisplay:
        steps = 0
        display(queens, startTime)
    
    limit = n
    count = 0
    resets = 0
    excludeQueen = None
    while not isSolved(queens):
        queens, excludeQueen = mutate(queens, excludeQueen)
        count =+ 1
        if count > limit:
            queens = getRandomAssignment(n)
            resets += 1
            count = 0

        if doDisplay:
            display(queens, startTime)
            steps += 1

    if doDisplay:
        print 'steps: {0}, resets: {1}, initial: {2}'.format(steps, resets, initialQueens)
    
    return queens

def display(queens, time):
    timeDiff = datetime.now() - time

    queens_range = range(0, len(queens))
    board = ''
    for row in queens_range:
        for col in queens_range:
            rowQ = queens[col]
            board += '|'
            board += 'Q' if rowQ == row else '.'
        board += '|\n'

    print timeDiff
    print queens
    print board

class Test(unittest.TestCase):
    def test_4(self):
        self.nQueens(4, True)

    def test_8(self):
        self.nQueens(8, True)

    def b(self, n):
        benchmark(lambda: solve(n, False), 1000)

    def test_b10(self):
        self.b(10)

    def test_b100(self):
        self.b(100)

    def test_b1000(self):
        self.b(1000)

    def test_b10000(self):
        self.b(10000)

    def test_solved(self):
        pass
        #queens = 
        #display(queens, datetime.now())
        #self.assertEqual(1, queens.fitness)

    def test_minconflict(self):
        queens = [3, 0, 1, 3]
        possibleAnswers = [1, 3]
        answer = minConflictValue(3, queens)
        print answer
        self.assertTrue(answer in possibleAnswers)

    def test_config(self):
        queens = [3, 7, 6, 0, 2, 9, 1, 5, 4, 8]
        solve(10, True, queens)

    def nQueens(self, n, doDisplay):
        solution = solve(n, doDisplay)

        self.assertTrue(isSolved(solution))

def benchmark(function, times=100):
    averageTime = 0
    for i in range(1, times+1):
        startTime = datetime.now()
        function()
        timeDiff = (datetime.now() - startTime).total_seconds()
        averageTime = ((i-1) * averageTime + timeDiff) / i # iterative average computation
        if i < 10 or i % 10 == 0:
            print '{0}\t{1}'.format(i, averageTime)

t = Test

if __name__ == '__main__':
    '''
    python NQueens
        -n [number of queens]
        [unittest options]
            Test.[test to run] (or t.[])
                test_fitness
                test_[4/8]
                test_b[10/100/1000/10000] (benchmark)
    '''
    if len(sys.argv) > 1 and sys.argv[1] == '-n':
        try:
            solve(int(sys.argv[2]), True)
        except IndexError as e:
            print 'when using -n option, provide n value after it'
    else:
        unittest.main(argv=sys.argv)
