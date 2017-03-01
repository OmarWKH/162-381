def foodHeuristic(state, problem):
    # max_distance(pacman, food) optimized
    gameState = problem.startingGameState
    foodList = foodGrid.asList()
    info = problem.heuristicInfo
    if info.get('distances') is None:
        info['distances'] = dict()
        for a in range(0, len(foodList)):
            for b in range(a, len(foodList)):
                foodA = foodList[a]
                foodB = foodList[b]
                pair = frozenset([foodA, foodB])
                info['distances'][pair] = mazeDistance(foodA, foodB, gameState)
    maxDistanceToFood = 0
    if position in foodList:
        for food in foodList:
            pair = frozenset([position, food])
            maxDistanceToFood = max(maxDistanceToFood, info['distances'][pair])
    else:
        distancesToFood = {food: mazeDistance(position, food, gameState) for food in foodGrid.asList()}
        furthestFood = max(distancesToFood, key=distancesToFood.get)
        pair = frozenset([position, furthestFood])
        maxDistanceToFood = distancesToFood[furthestFood]
        info['distances'][pair] = maxDistanceToFood
    return maxDistanceToFood

    # avrg_all_distance(pacman, food)
    gameState = problem.startingGameState
    distanceToFood = [mazeDistance(position, foodPoint, gameState) for foodPoint in foodGrid.asList()]
    return sum(distanceToFood) / len(distanceToFood) # 8396

    # max_distance(pacman, food)
    gameState = problem.startingGameState
    distanceToFood = [mazeDistance(position, foodPoint, gameState) for foodPoint in foodGrid.asList()]
    return max(distanceToFood) # 4137

    # min_distance(pacman, food)
    gameState = problem.startingGameState
    distanceToFood = [mazeDistance(position, foodPoint, gameState) for foodPoint in foodGrid.asList()]
    return min(distanceToFood) # 12372

    """
    Tried
        remaining food
        MD (furthest)
        1/num_legal moves
        distance between 2 pallets (closets, furthest)
    Untried
        food pallets in section
    """
    md = util.manhattanDistance
    ed = lambda xy1, xy2: ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

    foodPositions = foodGrid.asList()
    if len(foodPositions) == 0:
        return 0
    
    # return 1.0 / (len(foodPositions)) # same if uneaten food

    # empty = 0
    # dot = 0
    # wall = 0
    # for neighbor in _getNineNeighbors(position):
    #     if neighbor in foodPositions:
    #         dot += 1
    #     elif problem.walls[neighbor[0]][neighbor[1]]:
    #         wall += 1
    #     else:
    #         empty += 1
    # h = empty - dot - wall


    # if problem.heuristicInfo.get('lastFood') is None:
    #     problem.heuristicInfo['lastFood'] = position
    # elif position in foodGrid.asList():
    #     problem.heuristicInfo['lastFood'] = position
    # lastFood = problem.heuristicInfo['lastFood']
    # distancesToLastFood = {food: md(food, lastFood) for food in foodPositions} # could save distances in hInfo since they do not change
    # closestFood = min(distancesToLastFood, key=distancesToLastFood.get)
    # closestDistance = distancesToLastFood[closestFood]
    
    # h = max(closestDistance, md(position, closestFood))
    # /2
    # difference
    # max
    # withPacman = closestDistance + util.manhattanDistance(closestFood, position) # not admissable
    # if problem.heuristicInfo.get('positions') is None:
    #     problem.heuristicInfo['positions'] = set(position)
    # else:
    #     problem.heuristicInfo['positions'].add(position)
    # visitedPositions = problem.heuristicInfo['positions']
    # cost = 2 if position in visitedPositions else 0

    # all food distances
    # distance between 2 furthest food
    # distance between batman and 2nd most far fruit



    distanceToFood = {food: md(food, position) for food in foodPositions}
    
    foodQ = util.PriorityQueueWithFunction(lambda xy: md(xy, position))
    for food in foodPositions:
        foodQ.push(food)
    foodQ.push(position)

    h = 0
    while not foodQ.isEmpty():
        p1 = foodQ.pop()
        if not foodQ.isEmpty():
            p2 = foodQ.pop()
        h += md(p1, p2)
    return h / len(foodPositions)

    h = 0
    i = 1
    for d in sorted(distanceToFood.values(), reverse=True):
        h += i * d
        i *= -1
    return h

    furthest = max(distanceToFood, key=distanceToFood.get)
    distanceFurthestFood = {food: md(food, furthest) for food in distanceToFood}
    closestToFurthest = min(distanceFurthestFood, key=distanceFurthestFood.get)
    return md(closestToFurthest, position)

    #furthestFood = max(distanceToFood, key=distanceToFood.get)
    #furthestDistance = distanceToFood[furthestFood] # 9551
    # return furthestDistance
    closestFood = max(distanceToFood, key=distanceToFood.get)
    return mazeDistance(position, closestFood, problem.startingGameState)
    h = furthestDistance * cost
    distances = sorted(distanceToFood.values())
    # h = sum(distanceToFood.values())
    if len(distances) > 1:
        h = distances[0] + distances[1]
    else:
        h = distances[0]
    # h = sum(distanceToFood.values())/len(distanceToFood) # 11632
    
    # distanceToPrevious = md(position, lastFood)
    # distanceToNext = furthestDistance
    # h = 2 * distanceToPrevious + furthestDistance # 10757
    #h = max(distanceToPrevious, furthestDistance)

    """
    Previously tried code:
        num_food_on_axis = 0
        for food in foodXY:
            if food[0] == position[0] or food[1] == position[1]:
                num_food_on_axis += 1
        h_food_no_axis = len(foodXY) - num_food_on_axis

        if len(foodXY) == 1:
            return distances.values()[0]
        h_d2 = sorted(distances.values(), reverse=True)[-1] - sorted(distances.values(), reverse=True)[0]

        num_food = len(foodXY) # 12517

        num_legal = 4
        x,y = position
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = problem.walls[nextx][nexty]
            if hitsWall:
                num_legal -= 1

        h_num_legal = 10.0/num_legal # 16000
    """
    # distanceToFood = {food: mazeDistance(food, position, problem.startingGameState) for food in foodPositions}
    # furthestFood = max(distanceToFood, key=distanceToFood.get)
    # furthestDistance = distanceToFood[furthestFood] # 9551
    # h = furthestDistance
    
    return h

def mazeDistanceAStar(point1, point2, gameState, heuristic):
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.astar(prob, heuristic))
