'''
* = selected

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
    return 0

def mutate(configuration):
    pass
    
def minConflict(queen, queens):
    pass

def solve(n, doDisplay):
    startTime = datetime.now()
    random.seed()

    initialQueens = getRandomAssignment(n)
    initial = Configuration(initialQueens, getFitness(initialQueens))

    if doDisplay:
        display(initial, startTime)
    '''
    while not solved:
        child <- mutate
        if better(child.fitness, parent.fitness): change, display(initialQueens, startTime)
    return solution
    '''
    return initial

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

    print board
    print timeDiff
    print configuration.fitness

class Configuration:
    def __init__(self, queens, fitness):
        self.queens = queens
        self.fitness = fitness

class Test(unittest.TestCase):
    def test_8(self):
        self.nQueens(8, True)

    def test_b(self):
        benchmark(lambda: self.nQueens(8, False), 1000)

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

if __name__ == '__main__':
    unittest.main(argv=sys.argv)
