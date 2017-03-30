from random import randint, choice
from math import sqrt

def generate_hard_to_traverse_cells(grid, terrain_num, terrain_column_constraint, terrain_row_constraint, terrain_probability):
	"""[summary]

	[description]

	Arguments:
		grid {[type]} _- [description]
		terrain_column_constraint {[type]} -- [description]
		terrain_row_constraint {[type]} -- [description]
		terrain_probability {[type]} -- [description]
	"""
	total_columns = len(grid)
	total_rows = len(grid[0])

	hard_to_traverse_centers = []

	# generate terrain_num hard to traverse figures
	for index in range(terrain_num):

		# randomly generate position of center of hard to traverse figure
		column_pos = randint(0, total_columns-1)
		row_pos = randint(0, total_rows-1)

		while (column_pos, row_pos) in hard_to_traverse_centers:
			column_pos = randint(0, total_columns-1)
			row_pos = randint(0, total_rows-1)

		hard_to_traverse_centers.append((column_pos, row_pos))

		# calculate distance from boundary of figure to center of figure
		figure_column_distance_to_center = (terrain_column_constraint-1)/2
		figure_row_distance_to_center = (terrain_row_constraint-1)/2

		# using distance to center, calculate lower and upper bounds of figure
		figure_column_lower_bound = column_pos - figure_column_distance_to_center
		figure_row_lower_bound = row_pos - figure_row_distance_to_center

		figure_column_upper_bound = column_pos + figure_column_distance_to_center
		figure_row_upper_bound = row_pos + figure_row_distance_to_center

		# initially set total number of columns and rows to the constraints passed in
		figure_total_columns = terrain_column_constraint
		figure_total_rows = terrain_row_constraint

		# determine if upper and lower bounds are out of grid boundaries and adjust accordingly
		if(figure_column_lower_bound < 0):
			figure_total_columns += figure_column_lower_bound
			figure_column_lower_bound = 0

		if(figure_column_upper_bound > total_columns):
			figure_total_columns -= figure_column_upper_bound - total_columns
			figure_column_upper_bound = total_columns-1

		if(figure_row_lower_bound < 0):
			figure_total_rows += figure_row_lower_bound
			figure_top_left_row = 0

		if(figure_row_upper_bound > total_rows):
			figure_total_rows -= figure_row_upper_bound - total_rows
			figure_row_upper_bound = total_rows-1

		# for each column in the figure, and each row in the figure, determine with a 50% if a cell is hard to traverse
		for column in range(figure_column_lower_bound, figure_column_upper_bound):
			for row in range(figure_row_lower_bound, figure_row_upper_bound):
				if(randint(0,1) == 1):
					setattr(grid[column][row], 'terrain_type', '2')

	return hard_to_traverse_centers

def generate_highways(grid, number_highways, highway_segment_length, highway_total_length, same_direction_probability, turn_direction_probability):
	"""[summary]

	[description]

	Arguments:
		grid {[type]} -- [description]
		same_direction_probability {[type]} -- [description]
		turn_direction_probability {[type]} -- [description]
	"""
	total_columns = len(grid)
	total_rows = len(grid[0])

	while True:
		highway_attempts = 100
		highways = []
		completed_highways = False

		while highway_attempts > 0:
			completed_highway = False
			temp_highway = []

			while not completed_highway:
				#randomly decide placement of start for highway and direction that is away from boundary
				random_cell = randint(0,total_columns*2+total_rows*2-1)
				highway_start_pos = (random_cell, 0)
				highway_direction = (0, 1)

				if(random_cell >= total_columns) and (random_cell < total_columns*2):
					highway_start_pos = (random_cell-total_columns-1, total_rows-1)
					highway_direction = (0, -1)
				elif(random_cell >= total_columns*2) and (random_cell < total_columns*2+total_rows):
					highway_start_pos = (0, random_cell-total_columns*2)
					highway_direction = (1, 0)
				elif(random_cell >= total_columns*2+total_rows):
					highway_start_pos = (total_columns-1, random_cell-total_columns*2-total_rows)
					highway_direction = (-1, 0)

				#check that highway start position is not already used
				valid_highway_start_pos = True
				for highway in highways:
					if highway_start_pos == highway[0]:
						valid_highway_start_pos = False
						break
				if not valid_highway_start_pos:
					highway_attempts -= 1
					break

				#begin adding in start segment of highway
				highway_current_pos = highway_start_pos
				valid_highway_start_segment = True
				completed_highway_start_segment= False
				highway_start_segment = []
				highway_start_segment.append(highway_current_pos)

				#add cells according to segment length
				for cell in range(0, highway_segment_length-1):
					#set current position of new highway cell according to direction
					highway_current_pos = ((highway_current_pos[0] + highway_direction[0]), (highway_current_pos[1] + highway_direction[1]))
					if highway_current_pos[0] > 0 and highway_current_pos[1] > 0 and highway_current_pos[0] < total_columns-1 and highway_current_pos[1] < total_rows-1:
						#check that terrain type is valid
						cell_terrain = getattr(grid[highway_current_pos[0]][highway_current_pos[1]], 'terrain_type')
						if cell_terrain != 0:
							#check that cell is not already used in highway
							for highway in highways:
								if highway_current_pos in highway:
									valid_highway_start_segment = False
									break
							#if already exists, break and start again
							if valid_highway_start_segment:
								highway_start_segment.append(highway_current_pos)
							else:
								break
						else:
							valid_highway_start_segment = False
							break
					else:
						#inital start direction is entailed to never make start highway go out of bounds
						highway_start_segment.append(highway_current_pos)
						if len(highway_start_segment) >= highway_total_length:
							valid_highway_start_segment = True
							completed_highway = True
							break
						else:
							continue

				if not valid_highway_start_segment:
					highway_attempts -= 1
					break
				elif completed_highway:
					for cell in highway_start_segment:
						temp_highway.append(cell)
					break
				else:
					completed_highway_start_segment = True

				#add in turns
				highway_turn_attempts = 100
				highway_turn_segment = []
				while highway_turn_attempts > 0:
					completed_highway_turn_segment = False

					while not completed_highway_turn_segment:
						temp_turn = []
						highway_turn_current_pos = highway_current_pos
						highway_turn_direction = highway_direction
						valid_highway_turn_segment = True

						while True:
							make_turn = randint(0, 9)
							while make_turn >= 7:
								make_turn = randint(0, 9)

							if(make_turn > 5) and (make_turn < 8):
								new_highway_direction = randint(0, 1)
								#left turn
								if(new_highway_direction == 0):
									if(highway_turn_direction == (0, -1)):
										highway_direction = (-1, 0)
									elif(highway_direction == (0, 1)):
										highway_turn_direction = (1, 0)
									elif(highway_direction == (1, 0)):
										highway_turn_direction = (0, -1)
									elif(highway_direction == (-1, 0)):
										highway_turn_direction = (0, 1)
								#right turn
								else:
									if(highway_direction == (0, -1)):
										highway_turn_direction = (1, 0)
									elif(highway_direction == (0, 1)):
										highway_turn_direction = (-1, 0)
									elif(highway_direction == (1, 0)):
										highway_turn_direction = (0, 1)
									elif(highway_direction == (-1, 0)):
										highway_turn_direction = (0, -1)

								#if start highway is along boundary
								if highway_turn_current_pos[0] == 0:
									highway_turn_direction = (1, 0)
								elif highway_turn_current_pos[0] == total_columns-1:
									highway_turn_direction = (-1, 0)
								elif highway_turn_current_pos[1] == 0:
									highway_turn_direction = (0, 1)
								elif highway_turn_current_pos[1] == total_rows-1:
									highway_turn_direction = (0, -1)

							for cell in range(0, highway_segment_length):
								highway_turn_current_pos = (highway_turn_current_pos[0] + highway_turn_direction[0], highway_turn_current_pos[1] + highway_turn_direction[1])
								if highway_turn_current_pos[0] > 0 and highway_turn_current_pos[1] > 0 and highway_turn_current_pos[0] < total_columns-1 and highway_turn_current_pos[1] < total_rows-1:
									cell_terrain = getattr(grid[highway_turn_current_pos[0]][highway_turn_current_pos[1]], 'terrain_type')
									if cell_terrain != 0:
										if highway_turn_current_pos in temp_turn:
											valid_highway_turn_segment = False
											break
										for highway in highways:
											if highway_turn_current_pos in highway:
												valid_highway_turn_segment = False
												break
										temp_turn.append(highway_turn_current_pos)
									else:
										valid_highway_turn_segment = False
										break
								else:
									temp_turn.append(highway_turn_current_pos)
									completed_highway_turn_segment = True
									break
							if not valid_highway_turn_segment:
								break
							elif completed_highway_turn_segment:
								break

						if not valid_highway_turn_segment:
							highway_turn_attempts -= 1
							break
						elif completed_highway_turn_segment:
							for cell in temp_turn:
								highway_turn_segment.append(cell)
					else:
						break

				if completed_highway_turn_segment:
					if len(highway_start_segment) + len(highway_turn_segment) >= highway_total_length:
						completed_highway = True
						#append start segment
						for cell in highway_start_segment:
							temp_highway.append(cell)
						for cell in highway_turn_segment:
							temp_highway.append(cell)
						break
				else:
					highway_attempts -= 1
					break
			if completed_highway:
				highways.append(temp_highway)
			if len(highways) == number_highways:
				completed_highways = True
				break
		if completed_highways:
			for highway in highways:
				for cell in highway:
					cell_terrain = getattr(grid[cell[0]][cell[1]], 'terrain_type')
					if(cell_terrain == '1'):
						setattr(grid[cell[0]][cell[1]], 'terrain_type', 'a')
					elif(cell_terrain == '2'):
						setattr(grid[cell[0]][cell[1]], 'terrain_type', 'b')
					else:
						print "error ", cell, "terrain type ", cell_terrain
			break

def generate_blocked_cells(grid, percentage_blocked_cells):
	"""Randomly generates blocked cells in 2d list

	Calculates total amount of blocked cells based on percentage parameter.
	Then randomly chooses cells based on the entire grid.
	Only cells that are not highways or blocked cells can be converted to blocked.

	Arguments:
		grid {list[list]} -- 2d list meant to act as grid
		percentage_blocked_cells {float} -- percentage of the total number cells that can be blocked
	"""
	total_columns = len(grid)
	total_rows = len(grid[0])
	total_cells = total_columns * total_rows

	total_blocked_cells = int(total_cells * percentage_blocked_cells)

	for cell in range(0, total_blocked_cells):
		column = randint(0, total_columns-1)
		row = randint(0, total_rows-1)

		# continue checking if cell is a highway or already blocked cell else change to blocked
		while (getattr(grid[column][row], 'terrain_type') == 'a') or (getattr(grid[column][row], 'terrain_type') == 'b') or (getattr(grid[column][row], 'terrain_type') == '0'):
			column = randint(0, total_columns-1)
			row = randint(0, total_rows-1)
		else:
			setattr(grid[column][row], 'terrain_type', '0')


def generate_start_and_goal(grid, num_start_and_goals, column_bound, row_bound, min_distance):
	"""[summary]

	[description]

	Arguments:
		grid {[type]} -- [description]
		min_distance {[type]} -- [description]
	"""
	start_and_goals = []
	while len(start_and_goals) != 10:
		start = ()
		goal = ()
		i = 0

		while (goal == ()):
			column_pos = randint(0, column_bound*2)
			row_pos = randint(0, row_bound*2)

			if(column_pos >= column_bound):
				column_pos = (len(grid)-1-column_bound) + (column_pos-column_bound)
			if(row_pos >= row_bound):
				row_pos = (len(grid[0])-1-row_bound) + (row_pos-row_bound)

			if getattr(grid[column_pos][row_pos], 'terrain_type') == '0':
				continue
			elif(i == 0):
				start = (column_pos, row_pos)
				i = 1
			else:
				if(start != (column_pos, row_pos)):
					if(sqrt((column_pos - start[0])**2 + (row_pos - start[1])**2) >= 100):
						goal = (column_pos, row_pos)

		start_and_goal = (start, goal)
		if start_and_goal in start_and_goals:
			continue
		else:
			start_and_goals.append(start_and_goal)

	return start_and_goals
