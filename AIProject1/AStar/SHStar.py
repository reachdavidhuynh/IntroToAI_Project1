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
    self.h = 0

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

  def calc_f(self, weight):
    self.f = self.g + weight * self.h

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


  def __lt__(self, other):
    return self.f < other.f

  def __eq__(self, other):
    return self.x_pos == other.x_pos and self.y_pos == other.y_pos

def sequential_heuristic_astar(map, num_heuristics, start_pos, goal_pos, weight, weight_2):
  weight = 4
  weight_2 =1
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
  num_rows = len(map)
  num_columns = len(map[0])
  open_sets = []
  closed_sets = []
  g_values = []
  path = []

  for i in range(num_heuristics+1):
    open_sets.append([])
    start_node = Node(int(start_pos[0]), int(start_pos[1]), map[int(start_pos[1])][int(start_pos[0])][0], 0)
    start_node.calc_h(i, int(start_pos[0]), int(start_pos[1]), int(goal_pos[0]), int(goal_pos[1]))
    start_node.calc_f(weight)
    heappush(open_sets[i], start_node)
    closed_sets.append([])
    g_values.append([])
    g_values[i] = {start_pos[0]+","+start_pos[1]:0, goal_pos[0]+","+goal_pos[1]:INFINITY}
    path.append([])
    path[i] = {start_pos[0]+","+start_pos[1]:None, goal_pos[0]+","+goal_pos[1]:None}
    path[i][start_pos[0]+","+start_pos[1]] = [None, start_node]

  directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

#While open0.minkey < infinity
  while open_sets[0][0].f < INFINITY:
    #For i = 0 ... n
    for heuristic in range(1, num_heuristics):
      g_value_goal = g_values[heuristic][goal_pos[0]+","+goal_pos[1]]
      if len(open_sets[heuristic]) > 0 and (open_sets[heuristic][0].f <= weight_2 * open_sets[0][0].f):

        if g_value_goal <= open_sets[heuristic][0].f:
          #If goal value is less than infinity
          if g_value_goal < INFINITY:
            node_info = path[heuristic][goal_pos[0]+","+goal_pos[1]]
            while node_info[0] != None:
              print node_info[1].x_pos, node_info[1].y_pos
              map[node_info[1].y_pos][node_info[1].x_pos] = ('3', node_info[1].f, node_info[1].g, node_info[1].h)
              if int(node_info[1].x_pos) != int(start_pos[0]) and int(node_info[1].y_pos) != int(start_pos[1]):     
                node_info = path[heuristic][str(node_info[0][0])+","+str(node_info[0][1])]
            #Terminate and return path
            return map    

        else:
          current_node = heappop(open_sets[heuristic])
          print "heuristic", heuristic, "current_node", current_node.x_pos, " ", current_node.y_pos
          try:
            open_sets[heuristic].remove(current_node)
          except:
            pass
          heapify(open_sets[heuristic])
          current_node_key = str(current_node.x_pos)+","+str(current_node.y_pos)
          for tuple, d in zip(directions, range(len(directions))):
            neighbor_x_pos = current_node.x_pos+tuple[0]
            neighbor_y_pos = current_node.y_pos+tuple[1]
            if (neighbor_x_pos < num_columns and neighbor_x_pos >= 0) and (neighbor_y_pos < num_rows and neighbor_y_pos >= 0):
              if map[neighbor_y_pos][neighbor_x_pos][0] != '0':
                neighbor_key = str(neighbor_x_pos)+","+str(neighbor_y_pos)
                neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_y_pos][neighbor_x_pos][0], current_node.g)
                neighbor.calc_cost(current_node.type, 8, d)
                neighbor.g += neighbor.cost
                neighbor.calc_h(heuristic, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
                neighbor.calc_f(weight)
                if neighbor_key not in g_values[heuristic]:
                  g_values[heuristic][neighbor_key] = INFINITY
                  path[heuristic][neighbor_key] = None
                if g_values[heuristic][neighbor_key] > g_values[heuristic][current_node_key] + neighbor.cost:
                  g_values[heuristic][neighbor_key] = neighbor.g
                  path[heuristic][neighbor_key] = [(current_node.x_pos, current_node.y_pos), neighbor]
                  #print "path instance: ", path[heuristic][neighbor_key][0][0], path[heuristic][neighbor_key][0][1]
                  #print closed_set[heuristic]
                  if neighbor_key not in closed_sets[heuristic]:
                    try:
                      open_sets[heuristic].remove(neighbor)
                    except:
                      pass
                    open_sets[heuristic].append(neighbor)
                    heapify(open_sets[heuristic])
              closed_sets[heuristic].append(current_node_key)
      else:
        g_value_goal = g_values[0][goal_pos[0]+","+goal_pos[1]]
        if g_value_goal <= open_sets[0][0].f:
          if g_value_goal < INFINITY:
            node_info = path[0][goal_pos[0]+","+goal_pos[1]]
            while node_info[0] != None:
              map[node_info[1].y_pos][node_info[1].x_pos] = ('3', node_info[1].f, node_info[1].g, node_info[1].h)
              node_info = path[0][str(node_info[0][0])+","+str(node_info[0][1])]
            final_time = time.time() - beginning_time
            print "Runtime ", final_time
            print "Path length ", path_length
            print "Nodes expanded/traversed ", num_nodes_traversed
            print "Total cost ", total_cost
            return map
        else:
          current_node = heappop(open_sets[0])
          print "heuristic", 0, "current_node", current_node.x_pos, " ", current_node.y_pos
          try:
            open_sets[0].remove(current_node)
          except:
            pass
          heapify(open_sets[0])
          current_node_key = str(current_node.x_pos)+","+str(current_node.y_pos)
          for tuple, d in zip(directions, range(len(directions))):
            neighbor_x_pos = current_node.x_pos+tuple[0]
            neighbor_y_pos = current_node.y_pos+tuple[1]
            if (neighbor_y_pos < num_rows and neighbor_y_pos >= 0) and (neighbor_x_pos < num_columns and neighbor_x_pos >= 0):
              if map[neighbor_y_pos][neighbor_x_pos][0] != '0':
                neighbor_key = str(neighbor_x_pos)+","+str(neighbor_y_pos)
                neighbor = Node(neighbor_x_pos, neighbor_y_pos, map[neighbor_y_pos][neighbor_x_pos][0], current_node.g)
                neighbor.calc_cost(current_node.type, 8, d)
                neighbor.g += neighbor.cost
                neighbor.calc_h(0, int(start_pos[1]), int(start_pos[0]), int(goal_pos[1]), int(goal_pos[0]))
                neighbor.calc_f(weight)
                if neighbor_key not in g_values[0]:
                  g_values[0][neighbor_key] = INFINITY
                  path[0][neighbor_key] = None
                if g_values[0][neighbor_key] > current_node.g + neighbor.cost:
                  g_values[0][neighbor_key] = neighbor.g
                  path[0][neighbor_key] = [(current_node.x_pos, current_node.y_pos), neighbor]
                  if neighbor_key not in closed_sets[0]:
                    try:      
                      open_sets[0].remove(neighbor)
                    except:
                      pass
                      open_sets[0].append(neighbor)
                    heapify(open_sets[0])
                    num_nodes_traversed+=1    
              closed_sets[0].append(current_node_key)
