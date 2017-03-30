"""Object used in grid
"""
class Node:
	def __init__(self, column_pos, row_pos, type='1'):
		"""Constructor of Node object

		Takes two int values representing node's location on grid.
		Terrain is initially set to regular unblocked

		Arguments:
			column_pos {int} -- column position
			row_pos {int} -- row position
		"""
		self.column_pos = column_pos
		self.row_pos = row_pos
		self.terrain_type = type
