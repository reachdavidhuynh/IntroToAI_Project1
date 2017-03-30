from Node import Node
from GridTerrainGenerator import generate_hard_to_traverse_cells, generate_highways, generate_blocked_cells, generate_start_and_goal
import os, errno

"""Handles grid operations

Is the handler class for grid operations such as initialization,
"""
class Grid:
	def __init__(self, column_length, row_length):
		"""Initializes grid

		Takes number of row sand columns and then creates grid of Node objects

		Arguments:
			column-length {int} -- number of columns in grid
			row-length {int} -- number of rows in grid
		"""
		if(column_length > 0 and row_length > 0):
			self.column_length = column_length
			self.row_length = row_length
			self.grid = []

			for column in range(0, column_length):
				self.grid.append([])
				for row in range(0, row_length):
					self.grid[column].append(Node(column,row))

	def init_hard_to_traverse_cells(self, terrain_num, terrain_column_constraint=31, terrain_row_constraint=31, terrain_probability=.50):
		"""Initilizes hard to traverse cells of grid

		[description]

		Keyword Arguments:
			terrain_column_constraint {int} -- column constraint that defines column range of figure used to generate hard to traverse cells (default: {31})
			terrain_row_constraint {int} -- row constraint that defines column range of figure used to generate hard to traverse cells (default: {31})
			terrain_probability {int} -- probability that decides whether or not figure constrained by inputs is a hard to traverse cell (default: {50})
		"""
		self.hard_to_traverse_centers = generate_hard_to_traverse_cells(self.grid, terrain_num, terrain_column_constraint, terrain_row_constraint, terrain_probability)

	def init_highways(self, number_highways=4, highway_segment_length=20, highway_total_length=100, same_direction_probability=.60, turn_direction_probability=.40):
		"""Initializes highways of grid

		[description]

		Keyword Arguments:
			same_direction_probability {int} -- [description] (default: {60})
			turn_direction_probability {int} -- [description] (default: {40})
		"""
		generate_highways(self.grid, number_highways, highway_segment_length, highway_total_length, same_direction_probability, turn_direction_probability)

	def init_blocked_cells(self, percentage_blocked_cells=.20):
		"""Initializes blocked cells

		[description]

		Arguments:
			percentage_blocked_cells {int} -- Total number of cells percentage of blocked cells
		"""
		generate_blocked_cells(self.grid, percentage_blocked_cells)

	def init_start_and_goal(self, num_start_and_goals=10, column_bound=20, row_bound=20, min_distance=100):
		"""Initializes start and goal nodes of grid

		[description]

		Keyword Arguments:
			min_distance {int} -- Lower bound of distance between start and goal node (default: {100})
		"""
		start_and_goals = generate_start_and_goal(self.grid, num_start_and_goals, column_bound, row_bound, min_distance)
		return start_and_goals

	def write_grid_to_file(self, filename, start_and_goal_id, start, goal):
		"""[summary]

		[description]

		Arguments:
			filename {[type]} -- [description]
		"""
		current_working_dir = os.path.dirname(os.path.abspath(__file__))
		project_working_dir = os.path.dirname(current_working_dir)
		map_files_folder = os.path.join(project_working_dir, "MapFiles")
		new_map_file_path = os.path.join(map_files_folder, filename+"_"+str(start_and_goal_id)+".txt")

		new_map_file = open(new_map_file_path, "w")
		new_map_file.write(str(start)+"\n")
		new_map_file.write(str(goal)+"\n")
		for htt in self.hard_to_traverse_centers:
			new_map_file.write(str(htt)+"\n")
		for row in range(0, len(self.grid[0])):
			rowstring = ""
			for column in range(0, len(self.grid)):
				rowstring+=self.grid[column][row].terrain_type
			new_map_file.write(rowstring+"\n")

		new_map_file.close()
