# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # min distance to food
        minFoodDistance = 1
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if len(foodDistances) != 0:
            minFoodDistance = min(foodDistances)

        # close ghosts
        closeGhosts = 1
        for ghostState in newGhostStates:
            distance = manhattanDistance(newPos, ghostState.getPosition())
            if distance <= 2:
                if ghostState.scaredTimer <= 0:
                    closeGhosts += distance

        return closeGhosts + 1.0/minFoodDistance + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        value, action = self.value(gameState, self.index, gameState.getNumAgents())
        return action

    def value(self, gameState, agent, numAgents):
        '''
          Return a value,action pair.

          For depth limit 2 and 2 agents, the value of agent will be between 0 and 3.
          0 (agent 1) and 1 (agent 2) in depth 1.
          2 (agent 1) and 3 (agent 2) in depth 2.
          So agent % numAgents will refer to current agent index.
          And agent/numAgents will refer to current depth.
        '''
        currentDepth = float(agent)/numAgents
        if currentDepth >= self.depth or len(gameState.getLegalActions(agent % numAgents)) == 0:
            valueActionPair = (self.evaluationFunction(gameState), None)
        elif agent % numAgents == 0:
            valueActionPair = self.maxValue(gameState, agent, numAgents)
        else:
            valueActionPair = self.minValue(gameState, agent, numAgents)
        return valueActionPair

    def maxValue(self, gameState, agent, numAgents):
        maxValue = -sys.maxint
        maxAction = None
        for action in gameState.getLegalActions(agent % numAgents):
            successor = gameState.generateSuccessor(agent % numAgents, action)
            value = self.value(successor, agent+1, numAgents)[0]
            if value > maxValue: # >=? random?
                maxValue = value
                maxAction = action
        return (maxValue, maxAction)

    def minValue(self, gameState, agent, numAgents):
        minValue = sys.maxint
        minAction = None
        for action in gameState.getLegalActions(agent % numAgents):
            successor = gameState.generateSuccessor(agent % numAgents, action)
            value = self.value(successor, agent+1, numAgents)[0]
            if value < minValue: # <=? random?
                minValue = value
                minAction = action
        return (minValue, minAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        value, action = self.value(gameState, self.index, gameState.getNumAgents())
        return action

    def value(self, gameState, agent, numAgents, alpha=-sys.maxint, beta=sys.maxint):
        '''
          Return a value,action pair.
          
          For depth limit 2 and 2 agents, the value of agent will be between 0 and 3.
          0 (agent 1) and 1 (agent 2) in depth 1.
          2 (agent 1) and 3 (agent 2) in depth 2.
          So agent % numAgents will refer to current agent index.
          And agent/numAgents will refer to current depth.
        '''
        currentDepth = float(agent)/numAgents
        if currentDepth >= self.depth or len(gameState.getLegalActions(agent % numAgents)) == 0:
            valueActionPair = (self.evaluationFunction(gameState), None)
        elif agent % numAgents == 0:
            valueActionPair = self.maxValue(gameState, agent, numAgents, alpha, beta)
        else:
            valueActionPair = self.minValue(gameState, agent, numAgents, alpha, beta)
        return valueActionPair

    def maxValue(self, gameState, agent, numAgents, alpha, beta):
        maxValue = -sys.maxint
        maxAction = None
        for action in gameState.getLegalActions(agent % numAgents):
            successor = gameState.generateSuccessor(agent % numAgents, action)
            value = self.value(successor, agent+1, numAgents, alpha, beta)[0]
            if value > maxValue: # >=? random?
                maxValue = value
                maxAction = action
            if maxValue > beta:
                return (maxValue, maxAction)
            alpha = max(alpha, maxValue)
        return (maxValue, maxAction)

    def minValue(self, gameState, agent, numAgents, alpha, beta):
        minValue = sys.maxint
        minAction = None
        for action in gameState.getLegalActions(agent % numAgents):
            successor = gameState.generateSuccessor(agent % numAgents, action)
            value = self.value(successor, agent+1, numAgents, alpha, beta)[0]
            if value < minValue: # <=? random?
                minValue = value
                minAction = action
            if minValue < alpha:
                return (minValue, minAction)
            beta = min(beta, minValue)
        return (minValue, minAction)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        value, action = self.value(gameState, self.index, gameState.getNumAgents())
        return action

    def value(self, gameState, agent, numAgents):
        '''
          Return a value,action pair.

          For depth limit 2 and 2 agents, the value of agent will be between 0 and 3.
          0 (agent 1) and 1 (agent 2) in depth 1.
          2 (agent 1) and 3 (agent 2) in depth 2.
          So agent % numAgents will refer to current agent index.
          And agent/numAgents will refer to current depth.
        '''
        currentDepth = float(agent)/numAgents
        if currentDepth >= self.depth or len(gameState.getLegalActions(agent % numAgents)) == 0:
            valueActionPair = (self.evaluationFunction(gameState), None)
        elif agent % numAgents == 0:
            valueActionPair = self.maxValue(gameState, agent, numAgents)
        else:
            valueActionPair = self.chanceValue(gameState, agent, numAgents)
        return valueActionPair

    def maxValue(self, gameState, agent, numAgents):
        maxValue = -sys.maxint
        maxAction = None
        for action in gameState.getLegalActions(agent % numAgents):
            successor = gameState.generateSuccessor(agent % numAgents, action)
            value = self.value(successor, agent+1, numAgents)[0]
            if value > maxValue: # >=? random?
                maxValue = value
                maxAction = action
        return (maxValue, maxAction)

    def chanceValue(self, gameState, agent, numAgents):
        actions = gameState.getLegalActions(agent % numAgents)
        total = 0
        for action in actions:
            successor = gameState.generateSuccessor(agent % numAgents, action)
            total += self.value(successor, agent+1, numAgents)[0]
        value = total / len(actions)
        return (value, None)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    # if ghost not scared
        # making them scared is good
    # if ghost scared
        # eating them is good
    return 1.0/(mazeDistanceToClosestDot(currentGameState)+1) + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

# search
from game import Actions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

def mazeDistanceToClosestDot(gameState):
    """
    Returns a path (a list of actions) to the closest dot, starting from
    gameState.
    """
    # Here are some useful elements of the startState
    startPosition = gameState.getPacmanPosition()
    food = gameState.getFood()
    walls = gameState.getWalls()
    problem = AnyFoodSearchProblem(gameState)

    path = bfs(problem)
    return len(path) if path else 0

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        return state in self.food.asList()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    path = bfs(problem)
    return len(path) if path else 0

class Node:
    """
    Used in search and relies on SearchProblem. Takes:
    - successor: Tuple (state, action, cost).
    - previous: Parent Node. None if this is the starting state.

    Has:
    - state: Anything depending on the problem.
    - path: List of actions leading to this state.
    - cost: Cumulative cost from start to current state.
    """
    def __init__(self, successor, previous):
        notRoot = previous is not None
        self.state, action, cost = successor
        self.path = previous.path + [action] if notRoot else []
        self.cost = previous.cost + cost if notRoot else cost

def genericGraphSearch(problem, fringe):
    """
    Takes a fringe that defines the strategy of node expansion.
    Relies on Node and SearchProblem.
    """
    startState = problem.getStartState()
    asSuccessor = (startState, None, 0)
    fringe.push(Node(asSuccessor, None))
    visited = set()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in visited:
            visited.add(node.state)
            for successor in problem.getSuccessors(node.state):
                fringe.push(Node(successor,node))
    return None

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    """
    stack = util.Stack()
    return genericGraphSearch(problem, stack)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    queue = util.Queue()
    return genericGraphSearch(problem, queue)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    g = lambda node: node.cost
    pqwf = util.PriorityQueueWithFunction(g)
    return genericGraphSearch(problem, pqwf)

def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    g = lambda node: node.cost
    f = lambda node: heuristic(node.state, problem) + g(node)
    pqwf = util.PriorityQueueWithFunction(f)
    return genericGraphSearch(problem, pqwf)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
