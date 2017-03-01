def cornersHeuristic(state, problem):
    """
    Previously tried code:
        distances = {corner: util.manhattanDistance(corner, pacman) for corner in unvisited}
        min_corner = min(distances, key=distances.get)
        dist_min_corner = distances[min_corner] # 1475
        edist_min_corner = dist_min_point(pacman, unvisited, euclideanDistance) # 1532

        max_w = 1
        w = 0.25
        d_h = 0
        ds = distances.values()
        for d in ds:
            d_h += (max_w - w)*d
            w += w

        num_unvisited = len(unvisited) # 1908

        num_walls = 0
        for corner in unvisited:
           minx = min(corner[0], pacman[0])
           miny = min(corner[1], pacman[1])
           maxx = max(corner[0], pacman[0])
           maxy = max(corner[1], pacman[1])

           for x in range(minx, maxx):
               for y in range(miny, maxy):
                    num_walls += 1 if walls[x][y] else 0
    """