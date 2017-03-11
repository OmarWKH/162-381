'''
* = selected

some enhance points:
    1- fitness
    2- minconflict
    3- changing current/child

Formulation:
    1- Tuples
    2- Grid
    3*- List with column/row as index
getRandomAssignment:
    1*- list
    2- ordered list
mutate:
    var: random (!)
    1- min_conflict(var)
    2- overall fitness
solve:
    1*- iterative
    2- recursive
    ..
    change if:
    1- better
    2- better or equal
getFitness:
    1- # of conflicts
    2- # of 0-conflict queens
    3- weights
    4- weights: diagonal, row, column
display:
    1- diff-conflict(var)
    2- # 0-conflict queens
    3- total # conflicts
benchmark:
    disable display by:
    1*- toggle boolean
    2- redirect output (stdout) to no where instead of comman line
Parallel:
    1- solve multiple, return earliest
    2- queen conflicts for loop
No solution/stuck:
    1- n-times
    2- time limit
    3- simulated ann..
    4- modify fitness
'''

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

    for queen in queens:
        fitness += numberOfConfilct(queen,queens, True)
    return fitness


def numberOfConfilct(indexOfQueen, queens, excludePrevious):
    conflicts = 0
    queen = (indexOfQueen, queens[indexOfQueen])
    indexOfNext = indexOfQueen + 1 if excludePrevious else 0
    for col, row in enumerate(queens[indexOfNext:], indexOfNext):
        otherQueen = (col, row)
        if(queen != otherQueen):
            if( abs(queen[0] - otherQueen[0]) == abs( queen[1] - otherQueen[1] ) ):   # x-x == y-y diagnoal
                conflicts += 1
            elif(queen[1] == otherQueen[1] ):# y = y row check
                conflicts += 1
    return conflicts

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
        print row, numConflicts
    print minRows

    return random.sample(minRows, 1)[0] #return the min row conficlt




def solve(n, doDisplay, initial=None):
    startTime = datetime.now()
    random.seed()

    initialQueens = initial or getRandomAssignment(n)
    current = Configuration(initialQueens)

    if doDisplay:
        display(current, startTime)
    '''
    while not solved:
        child <- mutate
        if better(child.fitness, parent.fitness): change, display(initialQueens, startTime)
    return solution
    '''
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
        queens = Configuration([0, 2, 1, 3])
        display(queens, datetime.now())
        self.assertEqual(0, queens.fitness)

    def test_minconflict(self):
        queens = [3, 0, 1, 3]
        possibleAnswers = [1, 3]
        answer = minConflictValue(3, queens)
        print answer
        self.assertTrue(answer in possibleAnswers)

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
