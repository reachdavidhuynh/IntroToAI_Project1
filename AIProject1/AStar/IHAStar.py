from heapq import heappush, heappop, heapify
from math import sqrt
import time

class Node:
  def __init__(self, x_pos, y_pos, type, g):
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.key = str(x_pos) + "," + str(y_pos)
    self.type = type
    self.g = g

  def calc_h(self, heuristic, start_x, start_y, goal_x, goal_y):
    if heuristic == 0:
      #calc_manhattan_distance()
      xd = goal_x - self.x_pos
      yd = goal_y - self.y_pos
      d = abs(xd) + abs(yd)
      self.h = d
    elif heuristic == 1:
      #calc_diagonal_distance()
      cost_diagonal = 1.414
      cost_non_diagonal = 1
      x_difference = abs(goal_x - self.x_pos)
      y_difference = abs(goal_y - self.y_pos)
      ddistance = cost_non_diagonal*(x_difference + y_difference) + (cost_diagonal - 2*cost_non_diagonal) * min(x_difference, y_difference)
      self.h = ddistance
    elif heuristic == 2:
      #calc_euclidian_distance()
      x_difference = abs(goal_x - self.x_pos)
      y_difference = abs(goal_y - self.y_pos)
      edistance = sqrt(x_difference**2 + y_difference**2)
      self.h = edistance
    elif heuristic == 3:
      #calc_chevyshev_disanct()
      x_difference = abs(goal_x - self.x_pos)
      y_difference = abs(goal_y - self.y_pos)
      self.h = max(x_difference, y_difference)
    elif heuristic == 4:
      #calc_cross_product()
      x_difference1 = self.x_pos - goal_x
      y_difference1 = self.y_pos - goal_y
      x_difference2 = start_x - goal_x
      y_difference2 = start_y - goal_y
      cross = abs(x_difference1*y_difference2 - x_difference2*y_difference1)
      self.h = cross

  def calc_cost(self, parenttype, dirs, d):
    if parenttype == '1' and self.type == '1':
        if dirs == 8 and d % 2 == 0:
            self.cost = 1
        else:
            self.cost = sqrt(2)
    elif (parenttype == '2' and self.type == '2'):
        if dirs == 8 and d % 2 == 0:
            self.cost = 2
        else:
            self.cost = sqrt(8)
    elif (parenttype == '1' and self.type == '2') or (parenttype == '2' and self.type == '1'):
        if dirs == 8 and d % 2 == 0:
            self.cost = 1.5
        else:
            self.cost = (sqrt(2) + sqrt(8)) / 2
    elif parenttype == 'a' and self.type == 'a':
        self.cost = .25
    elif (parenttype == 'b' and self.type == 'b'):
        self.cost = .5
    elif (parenttype == 'a' and self.type == 'b') or (parenttype == 'b' and self.type == 'a'):
        self.cost = .375
    elif (parenttype == 'a' and self.type == '1') or (parenttype == '1' and self.type == 'a'):
        if dirs == 8 and d % 2 == 0:
            self.cost = (1 + .25)/2
        else:
            self.cost = (sqrt(2) + sqrt(.125))/2
    elif (parenttype == 'b' and self.type == '1') or (parenttype == '1' and self.type == 'b'):
        if dirs == 8 and d % 2 == 0:
            self.cost = (1 + .5)/2
        else:
            self.cost = ((sqrt(2) + sqrt(8))/2 + sqrt(.5))/2
    elif (parenttype == 'a' and self.type == '2') or (parenttype == '2' and self.type == 'a'):
        if dirs == 8 and d % 2 == 0:
            self.cost = (1.5 + .25)/2
        else:
            self.cost = ((sqrt(2) + sqrt(8))/2 + sqrt(.125))/2
    elif (parenttype == 'b' and self.type == '2') or (parenttype == '2' and self.type == 'b'):
        if dirs == 8 and d % 2 == 0:
            self.cost = (2 + .5)/2
        else:
            self.cost = (sqrt(8) + sqrt(.5))/2

  def calc_f(self, weight):
    self.f = self.g + weight*self.h

  def __lt__(self, other):
    return self.f < other.f

  def __eq__(self, other):
    return self.x_pos == other.x_pos and self.y_pos == other.y_pos

def integrated_heuristic_astar(map, num_heuristics, start_pos, goal_pos, weight_1, weight_2):
  global beginning_time
  beginning_time = time.time()
  global final_time
  global num_nodes_traversed
  num_nodes_traversed = 0
  global total_cost
  total_cost = 0
  global path_length
  path_length = 0

  global INFINITY
  INFINITY = 999999999

  global g_values
  g_values = {start_pos[1]+","+start_pos[0]:0, goal_pos[1]+","+goal_pos[0]:INFINITY}

  global path
  path = {start_pos[1]+","+start_pos[0]:None, goal_pos[1]+","+goal_pos[0]:None}

  num_rows = len(map)
  num_columns = len(map[0])

  open_sets = []
  #open_set_references = []
  for i in range(num_heuristics):
    open_sets.append([])
    #open_set_references.append(dict())
    start_node = Node(int(start_pos[1]), int(start_pos[0]), map[int(start_pos[1])][int(start_pos[0])][0], 0)
    start_node.calc_h(i, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
    start_node.calc_f(weight_1)
    heappush(open_sets[i], start_node)
    path[start_pos[1]+","+start_pos[0]] = [None, start_node]
    #open_set_references[i][start_pos[0]+","+start_pos[1]] = start_node

  closed_set_anchor = dict()
  closed_set_inadm = dict()

  directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

  while open_sets[0][0].f < INFINITY:
    for heuristic in range(1, num_heuristics):
      g_value_goal = g_values[goal_pos[1]+","+goal_pos[0]]
      if len(open_sets[heuristic]) > 0 and (open_sets[heuristic][0].f <= weight_2 * open_sets[0][0].f):
        if g_value_goal <= open_sets[heuristic][0].f:
          if g_value_goal < INFINITY:
            node_info = path[goal_pos[1]+","+goal_pos[0]]
            while node_info[0] != None:
              path_length+=1
              total_cost += node_info[1].cost
              map[node_info[1].x_pos][node_info[1].y_pos] = ('3', node_info[1].f, node_info[1].g, node_info[1].h)
              node_info = path[str(node_info[0][0])+","+str(node_info[0][1])]
            final_time = time.time() - beginning_time
            print "Runtime ", final_time
            print "Path length ", path_length
            print "Nodes expanded/traversed ", num_nodes_traversed
            print "Total cost ", total_cost
            return map
        else:
          current_node = heappop(open_sets[heuristic])
          for i in range(num_heuristics):
            try:
              open_sets[i].remove(current_node)
            except:
              pass
            heapify(open_sets[i])
          current_node_key = str(current_node.x_pos)+","+str(current_node.y_pos)
          for tuple, d in zip(directions, range(len(directions))):
            neighbor_x_pos = current_node.x_pos+tuple[0]
            neighbor_y_pos = current_node.y_pos+tuple[1]
            if (neighbor_x_pos < num_rows and neighbor_x_pos >= 0) and (neighbor_y_pos < num_columns and neighbor_y_pos >= 0):
              #print "neighbor ", neighbor_x_pos, " ", neighbor_y_pos
              if map[neighbor_x_pos][neighbor_y_pos][0] != '0':
                #print "valid neighbor"
                neighbor_key = str(neighbor_x_pos)+","+str(neighbor_y_pos)
                neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_x_pos][neighbor_y_pos][0], current_node.g)
                neighbor.calc_cost(current_node.type, 8, d)
                neighbor.g += neighbor.cost
                neighbor.calc_h(heuristic, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
                #print neighbor.h
                neighbor.calc_f(weight_1)
                if neighbor_key not in g_values:
                  g_values[neighbor_key] = INFINITY
                  path[neighbor_key] = None
                if g_values[neighbor_key] > g_values[current_node_key] + neighbor.cost:
                  g_values[neighbor_key] = neighbor.g
                  path[neighbor_key] = [(current_node.x_pos, current_node.y_pos), neighbor]
                 # print "path instance: ", path[neighbor_key][0][0], path[neighbor_key][0][1]
                  #print closed_set_anchor
                  if neighbor_key not in closed_set_anchor:
                   # print "gets here "
                  #  print "f value ", neighbor.f
                    try:
                      open_sets[0].remove(neighbor)
                    except:
                      pass
                    open_sets[0].append(neighbor)
                    heapify(open_sets[0])

                    num_nodes_traversed+=1

                    if neighbor_key not in closed_set_inadm:
                      #rint "gets here 2"
                      for i in range(1, num_heuristics):
                        heuristic_neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_x_pos][neighbor_y_pos][0], neighbor.g)
                        heuristic_neighbor.calc_h(i, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
                       # print heuristic_neighbor.h
                        heuristic_neighbor.calc_f(weight_1)
                       # print "heuristic neighbor f ", heuristic_neighbor.f
                        if heuristic_neighbor.f <= weight_2*neighbor.f:
                          #print "gets here 3"
                          try:
                            open_sets[i].remove(heuristic_neighbor)
                          except:
                            pass
                          open_sets[i].append(heuristic_neighbor)
                          heapify(open_sets[i])

              closed_set_inadm[current_node_key] = None
      else:
        if g_value_goal <= open_sets[0][0].f:
          if g_value_goal < INFINITY:
            node_info = path[goal_pos[1]+","+goal_pos[0]]
            while node_info[0] != None:
              path_length+=1
              total_cost += node_info[1].cost
              map[node_info[1].x_pos][node_info[1].y_pos] = ('3', node_info[1].f, node_info[1].g, node_info[1].h)
              node_info = path[str(node_info[0][0])+","+str(node_info[0][1])]
            final_time = time.time() - beginning_time
            print "Runtime ", final_time
            print "Path length ", path_length
            print "Nodes expanded/traversed ", num_nodes_traversed
            print "Total cost ", total_cost
            return map
        else:
          current_node = heappop(open_sets[0])
          for i in range(num_heuristics):
            try:
              open_sets[i].remove(current_node)
            except:
              pass
            heapify(open_sets[i])
          current_node_key = str(current_node.x_pos)+","+str(current_node.y_pos)
          for tuple, d in zip(directions, range(len(directions))):
            neighbor_x_pos = current_node.x_pos+tuple[0]
            neighbor_y_pos = current_node.y_pos+tuple[1]
            if (neighbor_x_pos < num_rows and neighbor_x_pos >= 0) and (neighbor_y_pos < num_columns and neighbor_y_pos >= 0):
              if map[neighbor_x_pos][neighbor_y_pos][0] != '0':
                neighbor_key = str(neighbor_x_pos)+","+str(neighbor_y_pos)
                neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_x_pos][neighbor_y_pos][0], current_node.g)
                neighbor.calc_cost(current_node.type, 8, d)
                neighbor.g += neighbor.cost
                neighbor.calc_h(0, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
                neighbor.calc_f(weight_1)
                if neighbor_key not in g_values:
                  g_values[neighbor_key] = INFINITY
                  path[neighbor_key] = None
                if g_values[neighbor_key] > g_values[current_node_key] + neighbor.cost:
                  g_values[neighbor_key] = neighbor.g
                  path[neighbor_key] = [(current_node.x_pos, current_node.y_pos), neighbor]
                  if neighbor_key not in closed_set_anchor:
                    try:
                      open_sets[0].remove(neighbor)
                    except:
                      pass
                    open_sets[0].append(neighbor)
                    heapify(open_sets[0])

                    num_nodes_traversed+=1

                    if neighbor_key not in closed_set_inadm:
                      for i in range(1, num_heuristics):
                        heuristic_neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_x_pos][neighbor_y_pos][0], neighbor.g)
                        heuristic_neighbor.calc_h(i, int(start_pos[1]), int(start_pos[0]),  int(goal_pos[1]), int(goal_pos[0]))
                        #print neighbor.h
                        heuristic_neighbor.calc_f(weight_1)
                        if heuristic_neighbor.f <= weight_2*neighbor.f:
                          try:
                            open_sets[i].remove(heuristic_neighbor)
                          except:
                            pass
                          open_sets[i].append(heuristic_neighbor)
                          heapify(open_sets[i])

              closed_set_anchor[current_node_key] = None

def perform_analysis(map, num_heuristics, start_pos, end_pos, weight_1, weight_2, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list):
  integrated_heuristic_astar(map, num_heuristics, start_pos, end_pos, weight_1, weight_2)

  runtime_list.append(final_time)
  pathlength_list.append(path_length)
  num_nodes_traversed_list.append(num_nodes_traversed)
  cost_incurred_list.append(total_cost)
