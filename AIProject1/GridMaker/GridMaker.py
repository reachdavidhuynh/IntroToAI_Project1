from Grid import Grid

grid = Grid(160,120)
grid.init_hard_to_traverse_cells(8)
grid.init_highways()
grid.init_blocked_cells()
num_start_and_goals = raw_input("Enter number of start and goal pairs you want:\n")
start_and_goals = grid.init_start_and_goal(int(num_start_and_goals))
filename = raw_input("Enter a filename for the new map:\n")
for i in range(int(num_start_and_goals)):
  grid.write_grid_to_file(filename, i+1, start_and_goals[i][0], start_and_goals[i][1])
