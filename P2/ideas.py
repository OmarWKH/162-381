'''
* = selected

some enhance points:
    1- fitness
    2- minconflict
    3- changing current/child
    4- check on fitness from beginning and decide wither to continue or get new assignment
    5- divide the configuration to two or multiple:
        a- seprate to two (one are queens with conflicts above 3, the other is queens below 3)
        then solve the below 3 after solved add a queen from above 3 until done 

Formulation:
    1- Tuples
    2- Grid
    3*- List with column/row as index
getRandomAssignment:
    1*- list
    2- ordered list
numberOfConflicts:
    1- dir (cound diagonl as 4 vs count diagonal as 1)
    2- # of conflicting queens (even if same diagonal)
	3- 6 direction method of counting (4 diagonal, 2 sideways)
mutate:
    var: random (!)
    1- min_conflict(var)
    2- overall fitness
    ..
    don't pick last mutated variable
    ..
    multi variable mutation
	3- swap between queens
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
        1- var: MCV
        2- random
    2- queen conflicts for loop
No solution/stuck:
    1- n-times
    2- time limit
    3- simulated ann..
    4- modify fitness
'''
