from heapq import heappush, heappop # for priority queue
from math import *
import time
import random
import os, sys
import sys
sys.path.append("../TerrainVisualizer")

num_nodes_traversed = 0
beginning_time = None

class node:
    xPos = 0 # x position
    yPos = 0 # y position
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance
    estimate = 0
    type = 0
    #type 0 = blocked 1 = unblocked 2 = hard to traverse a = river, unblocked b = river, hard
    def __init__(self, xPos, yPos, distance, priority, type, parent_direction, parenttype):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
        self.type = type
        self.parent_direction = parent_direction
        self.parenttype = parenttype
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority

	# h value
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Manhattan distance
        d = abs(xd) + abs(yd)
        estimate = 0
        return(d)

    def estimate_diagonal(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = abs(xd) + abs(yd) + (sqrt(2) - 2) * (sqrt(xd**2 + yd**2))
        return(d)

    def estimate_time(self, xDest, yDest):
        if self.parent_direction != None:
            global beginning_time
            current_time = time.time() - beginning_time
            if self.parent_direction % 2 != 0 and current_time > .05:
                return(self.estimate(xDest, yDest) - sqrt(2) * .75)
            elif self.parent_direction % 2 != 0 and current_time > .1:
                return(self.estimate(xDest, yDest) - sqrt(2) * 1.25)
        return(self.estimate(xDest, yDest))

    def estimate_prefer_highways(self, xDest, yDest):
        if self.parent_direction != None:
            if self.type == 'a' or self.type == 'b':
                return self.estimate(xDest, yDest) - ((sqrt(2) + sqrt(.125))/2) - .25
            elif self.parent_direction % 2 != 0 and (self.parenttype == 'a' or self.parenttype == 'b'):
                return self.estimate(xDest, yDest) + ((sqrt(2) + sqrt(.125))/2) - .25
        return(self.estimate(xDest, yDest))

    def estimate_ignore_htt(self, xDest, yDest):
        decrement = 0.0
        if self.parenttype == '2' and self.type == '2':
            if self.parent_direction % 2 == 0:
                decrement = 1
            else:
                decrement = sqrt(8) - sqrt (2)
        elif self.parenttype == '1' and self.type == '2':
            if self.parent_direction % 2 == 0:
                decrement = .5
            else:
                decrement = (sqrt(2) + sqrt(8)) / 2 - sqrt(2)
        elif self.parenttype == 'a' and self.type == '2':
            if self.parent_direction % 2 == 0:
                decrement = (1.5 + .25)/2 - (1 + .25)/2
            else:
                decrement = ((sqrt(2) + sqrt(8))/2 + sqrt(.125))/2 - (sqrt(2) + sqrt(.125))/2
        elif self.parenttype == 'b' and self.type == '2':
            if self.parent_direction % 2 == 0:
                decrement = (2 + .5)/2 + (1 + .5)/2
            else:
                decrement = (sqrt(8) + sqrt(.5))/2 + ((sqrt(2) + sqrt(8))/2 + sqrt(.5))/2
        return self.estimate(xDest, yDest) - decrement

    def estimate_avoid_htt(self, xDest, yDest):
        if(self.type == '2'):
            return self.estimate(xDest, yDest) + 5
        else:
            return self.estimate(xDest, yDest)

	#f value
    def updatePriority(self, xDest, yDest):
        #self.heuristic = self.estimate(xDest, yDest)
        #self.heuristic = self.estimate_diagonal(xDest, yDest)
        #self.heuristic = self.estimate_time(xDest, yDest)
        #self.heuristic = self.estimate_prefer_highways(xDest, yDest)
        #self.heuristic = self.estimate_ignore_htt(xDest, yDest)
        #self.heuristic = self.estimate_avoid_htt(xDest, yDest)

        self.priority = self.distance + self.heuristic

    #g value
    def nextMove(self, dirs, d, parenttype): # d: direction to move
        if parenttype == '1' and self.type == '1':
            # if diagonal
            if dirs == 8 and d % 2 == 0:
                self.distance += 1
            # if not diagonal
            else:
                self.distance += sqrt(2)
        elif (parenttype == '2' and self.type == '2'):
            # if diagonal
            if dirs == 8 and d % 2 == 0:
                self.distance += 2
            # if not diagonal
            else:
                self.distance += sqrt(8)
        elif (parenttype == '1' and self.type == '2') or (parenttype == '2' and self.type == '1'):
            # if diagonal
            if dirs == 8 and d % 2 == 0:
                self.distance += 1.5
            # if not diagonal
            else:
                self.distance += (sqrt(2) + sqrt(8)) / 2


        elif parenttype == 'a' and self.type == 'a':
            self.distance += .25
            #.25
        elif (parenttype == 'b' and self.type == 'b'):
            self.distance += .5
            #.5
        elif (parenttype == 'a' and self.type == 'b') or (parenttype == 'b' and self.type == 'a'):
            self.distance += .375
            #.375

        elif (parenttype == 'a' and self.type == '1') or (parenttype == '1' and self.type == 'a'):
            if dirs == 8 and d % 2 == 0:
                self.distance += (1 + .25)/2
            else:
                self.distance += (sqrt(2) + sqrt(.125))/2

        elif (parenttype == 'b' and self.type == '1') or (parenttype == '1' and self.type == 'b'):
            if dirs == 8 and d % 2 == 0:
                self.distance += (1 + .5)/2
            else:
                self.distance += ((sqrt(2) + sqrt(8))/2 + sqrt(.5))/2

        elif (parenttype == 'a' and self.type == '2') or (parenttype == '2' and self.type == 'a'):
            if dirs == 8 and d % 2 == 0:
                self.distance += (1.5 + .25)/2
            else:
                self.distance += ((sqrt(2) + sqrt(8))/2 + sqrt(.125))/2

        elif (parenttype == 'b' and self.type == '2') or (parenttype == '2' and self.type == 'b'):
            if dirs == 8 and d % 2 == 0:
                self.distance += (2 + .5)/2
            else:
                self.distance += (sqrt(8) + sqrt(.5))/2


# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
    global num_nodes_traversed
    num_nodes_traversed = 0

    global beginning_time
    beginning_time = time.time()

    closed_nodes_map = [] # map of closed (tried-out) nodes
    open_nodes_map = [] # map of open (not-yet-tried) nodes
    dir_map = [] # map of dirs
    row = [0] * n
    for i in range(m): # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map_row = []
        for j in range(n):
            dir_map_row.append(None)
        dir_map.append(dir_map_row)

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0, '1', None, None)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority, n1.type, n1.parent_direction, n1.parenttype)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        closed_nodes_map[y][x] = 1 # mark it on the closed nodes map
        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the dirs
            path = []
            while not (x == xA and y == yA):
                j = dir_map[y][x].parent_direction
                #c = str((j + dirs / 2) % dirs)
                path.insert(0, dir_map[y][x])
                x += dx[j]
                y += dy[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1 or the_map[ydy][xdx][0] == 1 or closed_nodes_map[ydy][xdx] == 1 or the_map[ydy][xdx][0] == '0'): # if blocked cell don't go there
                # generate a child node with a type as last input
                m0 = node(xdx, ydy, n0.distance, n0.priority, the_map[ydy][xdx][0], (i + dirs / 2) % dirs, n0.type)
                # compare types between this new move and parent type
                m0.nextMove(dirs, i, the_map[y][x][0])
                m0.updatePriority(xB, yB)

                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    #dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    dir_map[ydy][xdx] = m0
                    num_nodes_traversed += 1
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction
                    # dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    dir_map[ydy][xdx] = m0
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found

# MAIN

def show_route(option, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list, user_input):

    #first position is to right of cell and then  moves counter clockwise
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

    n = 160 # horizontal size of the map
    m = 120 # vertical size of the map
    the_map = []

    from ASVisualizer import create_map
    the_map = create_map(user_input)
    from ASVisualizer import start_pos, end_pos
    start = 0
    end = 0
    start = start_pos(user_input)
    end = end_pos(user_input)
    xA = int(start[0])
    yA = int(start[1])
    xB = int(end[0])
    yB = int(end[1])

    t = time.time()
    route = pathFind(the_map, n, m, 8, dx, dy, xA, yA, xB, yB)
    finaltime = time.time() - t
    print 'Time to generate (seconds): ', finaltime
    if route == '':
        print "Could not find path"
    else:
        cost_incurred = 0.0
        # mark the route on the map
        if len(route) > 0:
            x = xA
            y = yA
            for i in range(len(route)):
                j = (route[i].parent_direction + 8 / 2) % 8
                x += dx[j]
                y += dy[j]
                the_map[y][x] = ('3', route[i].priority, route[i].distance, route[i].heuristic)
            else:
                cost_incurred = route[i].distance
        if option == 1:
            runtime_list.append(finaltime)
            pathlength_list.append(len(route))
            num_nodes_traversed_list.append(num_nodes_traversed)
            cost_incurred_list.append(cost_incurred)

	return the_map

