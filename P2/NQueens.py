import random
import unittest
from datetime import datetime
import sys
import csv
import collections

def getRandomAssignment(n):
    '''
    col == index
    row = queens[col]
    top left is (0, 0)
    '''
    rows = collections.defaultdict(lambda: 1)
    diagonalR = collections.defaultdict(lambda: 0)
    diagonalL = collections.defaultdict(lambda: 0)
    queens = random.sample(xrange(0, n), n)
    fitness = 0
    for col, row in enumerate(queens):
        dR = getDiagonalRight(col, row, n)
        dL = getDiagonalLeft(col, row)
        queen = (col, row)
        if sameDiagonal(queen, dR):
            diagonalR[dR] += 1
            if diagonalR[dR] > 1:
                fitness += 1
        if sameDiagonal(queen, dL):
            diagonalL[dL] += 1
            if diagonalL[dL] > 1:
                fitness += 1

    return (queens, rows, diagonalR, diagonalL, fitness)

def isSolved(queens):
    for column in xrange(0, len(queens)):
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

def numberOfConfilct(qCol, queens, maxConflicts=sys.maxint):
    conflicts = 0

    # (R)ight, (L)eft, U(p), D(own)
    rowR = False
    rowL = False
    diagonalUR = False
    diagonalUL = False
    diagonalDR = False
    diagonalDL = False

    qRow = queens[qCol]
    for oCol, oRow in enumerate(queens):
        allTrue = rowR and rowL and diagonalUR and diagonalUL and diagonalDR and diagonalDL
        if allTrue:
            break
        if conflicts > maxConflicts:
            return sys.maxint

        if oCol == qCol:
            continue

        if oCol < qCol:
            if oRow < qRow:
                if not diagonalUL:
                    diagonalUL = (qCol - oCol) == (qRow - oRow)
                    conflicts += 1 if diagonalUL else 0
            elif oRow > qRow:
                if not diagonalDL:
                    diagonalDL = (qCol - oCol) == (oRow - qRow)
                    conflicts += 1 if diagonalDL else 0
            else: # oRow == qRow
                if not rowL:
                    rowL = True
                    conflicts += 1
        else: #oCol > qCol
            if oRow < qRow:
                if not diagonalUR:
                    diagonalUR = (oCol - qCol) == (qRow - oRow)
                    conflicts += 1 if diagonalUR else 0
            elif oRow > qRow:
                if not diagonalDR:
                    diagonalDR = (oCol - qCol) == (oRow - qRow)
                    conflicts += 1 if diagonalDR else 0
            else: # oRow == qRoow
                if not rowR:
                    rowR = True
                    conflicts += 1

    return conflicts

def getDiagonalRight(x, y, n):
    if x + y < n - 1:
        return (0, x + y)
    elif x + y > n - 1:
        return (x + y - n - 1, n - 1)
    else:
        return (0, n - 1)

def getDiagonalLeft(x, y):
    if x > y:
        return (x - y, 0)
    elif y > x:
        return (0, y - x)
    else:
        return (0, 0)

def sameRow(queen1, queen2):
    return queen1[1] == queen2[1]

def sameDiagonal(queen1, queen2):
    return abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1])

def mutate(queens, excludeQueen=None):
    queen, altQueen = random.sample(queens[0], 2)
    queen = queen if queen != excludeQueen else altQueen
    newRow, offset = minConflictValue(queen, queens)
    return (queen, newRow, offset) # mutated, variable to exclue next, conflict change

def minConflictValue(queenColumn, queens):# n
    queenRow = queens[0][queenColumn]
    currentConflict = 0

    minConfilct = sys.maxint
    minRows = []
    for row in xrange(0, len(queens[0])):

        rowConflict = queens[1][row] + 1
        diagonalRConflict = queens[2][getDiagonalRight(queenColumn, row, len(queens[0]))] + 1
        diagonalLConflict = queens[3][getDiagonalLeft(queenColumn, row)] + 1

        numConflicts = rowConflict + diagonalRConflict + diagonalLConflict

        if row == queenRow:
            currentConflict = numConflicts

        if numConflicts < minConfilct:
            minConfilct = numConflicts
            minRows = [row]
        elif numConflicts == minConfilct:
            minRows.append(row)

    offset = minConfilct - currentConflict
    return (minRows[random.randrange(0, len(minRows))], offset)

def solve(n, doDisplay=True, displayBoard=True, displayQueens=True, seed=None):
    startTime = datetime.now()

    if seed:
        random.seed(seed)
    else:
        seed = random.randint(0, sys.maxint)
        random.seed(seed)

    queensAndConflicts = getRandomAssignment(n)
    
    if doDisplay:
        steps = 0
        display(queensAndConflicts[0], startTime, displayBoard=displayBoard, displayQueens=displayQueens)
    
    conflictBalance = 0
    limit = n
    count = 0
    resets = 0
    excludeQueen = None
    while not isSolved(queensAndConflicts[0]):
        excludeQueen, newRow, conflictOffset = mutate(queensAndConflicts, excludeQueen)

        if conflictOffset < 0: #improvement or same 
            conflictBalance += conflictOffset
            
            # change queen
            oldRow = queensAndConflicts[0][excludeQueen]
            queensAndConflicts[0][excludeQueen] = newRow
            # remove from old
            queensAndConflicts[1][oldRow] -= 1
            queensAndConflicts[2][getDiagonalRight(excludeQueen, oldRow, n)] -= 1
            queensAndConflicts[3][getDiagonalLeft(excludeQueen, oldRow)] -= 1
            # add to new
            queensAndConflicts[1][newRow] += 1
            queensAndConflicts[2][getDiagonalRight(excludeQueen, newRow, n)] += 1
            queensAndConflicts[3][getDiagonalLeft(excludeQueen, newRow)] += 1

            count = 0
            if doDisplay:
                display(queensAndConflicts[0], startTime, displayBoard=displayBoard, displayQueens=displayQueens)
        else:
            count =+ 1

        if count > limit:
            queensAndConflicts = getRandomAssignment(n)
            resets += 1
            count = 0

        if doDisplay:
            steps += 1

    if doDisplay:
        print 'steps: {0}, resets: {1}, seed: {2}'.format(steps, resets, seed)
    return (queensAndConflicts[0], seed)

def display(queens, time, displayBoard=True, displayQueens=True):
    timeDiff = datetime.now() - time

    queens_range = range(0, len(queens))
    queens = queens if displayQueens else ''
    board = ''
    if displayBoard:
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
        fileName = 'log/{0} -- {1}.csv'.format(str(datetime.now()).replace(':', '-'), n)
        with open(fileName, 'wb') as file:
            writer = csv.writer(file)
            writer.writerow(['i', 'solution', 'timeDiff', 'averageTime', 'seed'])
            for instance in benchmark(n, 1000, writer=writer):
                i, result, timeDiff, averageTime = instance
                solution, seed = result
                writer.writerow([i, solution, timeDiff, averageTime, seed])

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
        pass
        # give seed instead of initial
        #queens = [3, 7, 6, 0, 2, 9, 1, 5, 4, 8]
        #solve(10, True, initial=queens)

    def nQueens(self, n, doDisplay):
        solution = solve(n, doDisplay)
        self.assertTrue(isSolved(solution))

def benchmark(n, times=100, writer=None):
    averageTime = 0
    
    for i in xrange(1, times+1):
        startTime = datetime.now()

        seed = random.randint(0, sys.maxint)

        # write seed before solving, so if it gets stuck we could reproduce
        if writer:
            writer.writerow(['seed', i, seed])

        result = solve(n, False, seed=seed)
        
        timeDiff = (datetime.now() - startTime).total_seconds()
        averageTime = ((i-1) * averageTime + timeDiff) / i # iterative average computation

        yield (i, result, timeDiff, averageTime)

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
