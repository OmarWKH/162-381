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
    return random.sample(range(0, n), n)

def getFitness(queens):
    fitness = 0

    for column in range(0, len(queens)):
        fitness += numberOfConfilct(column, queens, True)

    return fitness

def numberOfConfilct(indexOfQueen, queens, excludePrevious):
    conflicts = 0
    queen = (indexOfQueen, queens[indexOfQueen])
    indexOfNext = indexOfQueen + 1 if excludePrevious else 0

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
        if not rowR:
            rowR = sameRow(queen, otherQueen) and queen[0] < otherQueen[0]
        if not rowL:
            rowL = sameRow(queen, otherQueen) and queen[0] > otherQueen[0]
        if not diagonalUR:
            diagonalUR = sameDiagonal(queen, otherQueen) and queen[0] < otherQueen[0] and queen[1] > otherQueen[1]
        if not diagonalDR:
            diagonalDR = sameDiagonal(queen, otherQueen) and queen[0] < otherQueen[0] and  queen[1] < otherQueen[1]
        if not diagonalUL:
            diagonalUL = sameDiagonal(queen, otherQueen) and queen[0] > otherQueen[0] and queen[1] > otherQueen[1]
        if not diagonalDL:
            diagonalDL = sameDiagonal(queen, otherQueen) and queen[0] > otherQueen[0] and queen[1] < otherQueen[1]
    conflicts = int(rowR) + int(rowL) + int(diagonalUR) + int(diagonalUL) + int(diagonalDR) + int(diagonalDL)
    return conflicts
'''
    sameRow = False
    sameDiagonal = False
    for col, row in enumerate(queens[indexOfNext:], indexOfNext):
        if(queen != otherQueen):
            if not sameRow:
                sameRow = sameRow(queen, otherQueen)
            if not sameDiagonal:
                sameDiagonal = sameDiagonal(queen, otherQueen)
            if abs(queen[0] - otherQueen[0]) == abs( queen[1] - otherQueen[1] && ):   # x-x == y-y diagnoal
                conflicts += 1
            elif(queen[1] == otherQueen[1]):    # y = y row check
                conflicts += 1
'''

def sameRow(queen1, queen2):
    return queen1[1] == queen2[1]

def sameDiagonal(queen1, queen2):
    return abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1])

def mutate(queens):
    queen = random.randrange(0, len(queens))
    row = minConflictValue(queen, queens)
    newQueens = list(queens)
    newQueens[queen] = row
    return newQueens

def minConflictValue(queenColumn, queens):# n
    minConfilct = sys.maxint
    queens = list(queens)
    minRows = []
    for row in range(0, len(queens)):
        queens[queenColumn] = row
        numConflicts = numberOfConfilct(queenColumn, queens, False)
        if numConflicts < minConfilct:
            minConfilct = numConflicts
            minRows = [row]
        elif numConflicts == minConfilct:
            minRows.append(row)

    return random.sample(minRows, 1)[0] #return the min row conficlt

def solve(n, doDisplay, initial=None):
    startTime = datetime.now()
    random.seed()

    initialQueens = initial or getRandomAssignment(n)
    current = Configuration(initialQueens)

    if doDisplay:
        steps = 0
        display(current, startTime)
    
    while current.fitness > 0:
        child = mutate(current.queens)
        child = Configuration(child)

        if doDisplay:
            steps += 1

        if doDisplay:
            display(child, startTime)
        current = child

    if doDisplay:
        print 'steps: {0}, initial: {1}'.format(steps, initialQueens)
    return current

def display(configuration, time):
    timeDiff = datetime.now() - time

    queens = configuration.queens
    queens_range = range(0, len(queens))
    board = ''
    for row in queens_range:
        for col in queens_range:
            rowQ = queens[col]
            board += '|'
            board += 'Q' if rowQ == row else '.'
        board += '|\n'

    print timeDiff, configuration.fitness
    print queens
    print board

class Configuration:
    def __init__(self, queens):
        self.queens = queens
        self.fitness = getFitness(queens)

class Test(unittest.TestCase):
    def test_4(self):
        self.nQueens(4, True)

    def test_8(self):
        self.nQueens(8, True)

    def b(self, n):
        benchmark(lambda: self.nQueens(n, False), 1000)

    def test_b10(self):
        self.b(10)

    def test_b100(self):
        self.b(100)

    def test_b1000(self):
        self.b(1000)

    def test_b10000(self):
        self.b(10000)

    def test_fitness(self):
        queens = Configuration([5, 2, 0, 7, 4, 7, 1, 6])
        display(queens, datetime.now())
        self.assertEqual(1, queens.fitness)

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
        optimalFitness = 0
        solution = solve(n, doDisplay)

        self.assertEqual(optimalFitness, solution.fitness)

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
