import random
import unittest
from datetime import datetime

def getRandomAssignment(n):
    random.seed()
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
    
def solve(initial, startTime):
    display(initial.queens, startTime)
    '''
    while not solved:
        child <- mutate
        if better(child.fitness, parent.fitness): change, display(initialQueens, startTime)
    return solution
    '''
    return initial

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
    print board
    print timeDiff

class Configuration:
    def __init__(self, queens, fitness):
        self.queens = queens
        self.fitness = fitness

class Test(unittest.TestCase):
    def test_8_queens(self):
        self.nQueens(8)

    def nQueens(self, n):
        startTime = datetime.now()
        initialQueens = getRandomAssignment(n)
        initial = Configuration(initialQueens, getFitness(initialQueens))
        optimalFitness = 0
        solution = solve(initial, startTime)
        
        self.assertEqual(optimalFitness, solution.fitness)

def benchmark():
    pass

if __name__ == '__main__':
    unittest.main()