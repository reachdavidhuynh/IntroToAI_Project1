import pygame, sys, os
sys.path.append("../AStar")
import Heuristics

class Visualizer(object):

	def __init__(self, all_map_directory_name="MapFiles"):
		self.all_map_directory_name = all_map_directory_name

	def init_map_structure(self, start_pos_line = 0, end_pos_line = 1, map_start_line = 10):
		self.start_pos_line = start_pos_line
		self.end_pos_line = end_pos_line
		self.map_start_line = map_start_line

	def init_gui_parameters(self, map_width=160, map_height=120, margin_width=1, tile_size=4):
		self.MAP_WIDTH = map_width
		self.MAP_HEIGHT = map_height
		self.MARGIN_WIDTH = margin_width
		self.TILE_SIZE = tile_size

	def init_gui_colors(self):
		BLACK = (0, 0, 0)
		GRAY = (153, 153, 153)
		WHITE = (255, 255, 255)
		BLUE = (0, 0, 255)
		LIGHTBLUE = (179, 179, 255)
		GREEN = (26, 255, 26)
		RED = (198, 0, 0)
		self.COLORS = {
			'0' : BLACK,
			'1' : WHITE,
			'2' : GRAY,
			'a' : BLUE,
			'b' : LIGHTBLUE,
			'R' : GREEN,
			'S' : GREEN,
			'3' : RED,
		}

	def init_default(self):
		self.init_map_structure()
		self.init_gui_parameters()
		self.init_gui_colors()

	def parse_start_pos(self, line):
		return line.strip('()').replace(')', '').replace('\n', '').split(', ', 1)

	def parse_end_pos(self, line):
		return line.strip('()').replace(')', '').replace('\n', '').split(', ', 1)

	def parse_map_file(self, map_group_name, map_file_name):
		current_working_dir = os.path.dirname(os.path.abspath(__file__))
		project_working_dir = os.path.dirname(current_working_dir)
		all_map_files_dir = os.path.join(project_working_dir, self.all_map_directory_name)
		map_file_path = os.path.join(all_map_files_dir, map_group_name, map_file_name)

		if not os.path.exists(map_file_path):
			print "Input file name or file directory does not exist at:\n", map_file_path
			return False

		self.map = []
		self.start_pos = []
		self.end_pos = []
		with open(map_file_path) as map_file:
			for i, line in enumerate(map_file):
				if i == self.start_pos_line:
					self.start_pos = self.parse_start_pos(line)
				elif i == self.end_pos_line:
					self.end_pos = self.parse_end_pos(line)
				elif i>= 10:
					s = list(line)
					s.remove('\n')
					row = []
					for terrain in s:
						row.append((terrain, None, None, None))
					self.map.append(row)
				"""elif i >= 11:
					s = list(line)
					s.remove('\n')
					for char, j in zip(s, range(len(s))):
						self.map[j].append((char, None, None, None))
				elif i >= 10:
					s = list(line)
					s.remove('\n')
					for j in range(len(s)):
						self.map.append([])
					for char, j in zip(s, range(len(s))):
						self.map[j].append((char, None, None, None))
				"""

		return True

	def get_heuristic(self, default_heuristic_name):
		self.heuristic_name = raw_input("What is the name of the heuristic you want to use?\n").replace(" ", "_")
		heuristic_function = None
		try:
			heuristic_function = getattr(Heuristics, self.heuristic_name)
			return heuristic_function
		except Exception as e:
			print "No implemented heuristic with that name.\n Using default heuristic "+default_heuristic_name+".\n"
			self.heuristic_name = default_heuristic_name.replace(" ", "_")
			heuristic_function = getattr(Heuristics, self.heuristic_name)
			return heuristic_function

	def get_weight(self):
		self.weight =  float(raw_input("What weight do you want to use?\n"))
		return self.weight

	def get_weight_1(self):
		self.weight_1 =  float(raw_input("What lower bound weight do you want to use?\n"))
		return self.weight_1

	def get_weight_2(self):
		self.weight_2 =  float(raw_input("What upper bound weight do you want to use?\n"))
		return self.weight_2

	def run_search(self):
		pass

	def display_map(self, caption="Grid"):
		self.map = self.run_search()
		if self.map == None:
			return False
		else:
			pygame.init()
			DISPLAYSURF = pygame.display.set_mode((self.MAP_WIDTH*(self.MARGIN_WIDTH+self.TILE_SIZE)+200 + (2 * self.TILE_SIZE), self.MAP_HEIGHT*(self.MARGIN_WIDTH+self.TILE_SIZE)+100))
			pygame.display.set_caption(caption)

			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
						#This allows us to click a cell
					elif event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						column = pos[0] // (self.TILE_SIZE + self.MARGIN_WIDTH)
						row = pos[1] // (self.TILE_SIZE + self.MARGIN_WIDTH)
						print("Click ", pos, "Grid coordinates: ", row, column)
						if row < self.MAP_HEIGHT and column < self.MAP_WIDTH:
							DISPLAYSURF.fill((0,0,0))
							myfont = pygame.font.SysFont("monospace", 16)
							label = myfont.render("Cell: ("+str(column)+", "+str(row)+")", 1, (255, 255, 255))
							DISPLAYSURF.blit(label, (800, 30))
							if len(self.map[row][column]) > 1:
								flabel = myfont.render("f = "+ str(self.map[row][column][1]), 1, (255, 255, 255))
								DISPLAYSURF.blit(flabel, (800, 50))
								glabel = myfont.render("g = "+ str(self.map[row][column][2]), 1, (255, 255, 255))
								DISPLAYSURF.blit(glabel, (800, 70))
								hlabel = myfont.render("h = "+ str(self.map[row][column][3]), 1, (255, 255, 255))
								DISPLAYSURF.blit(hlabel, (800, 90))
				for row in range(self.MAP_HEIGHT):
					for column in range(self.MAP_WIDTH):
						if str(row) == self.start_pos[1] and str(column) == self.start_pos[0]:
							color = (26, 255, 26)
						elif str(row) == self.end_pos[1] and str(column) == self.end_pos[0]:
							color = (0, 165, 255)
						else:
							color = self.COLORS[self.map[row][column][0]]
						pygame.draw.rect(DISPLAYSURF, color, (column*(self.MARGIN_WIDTH+self.TILE_SIZE) + self.MARGIN_WIDTH,row*(self.MARGIN_WIDTH+self.TILE_SIZE) + self.MARGIN_WIDTH,self.TILE_SIZE,self.TILE_SIZE))
				pygame.display.update()

	def run_search_analysis(self, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list, heuristic_function):
		pass

	def write_search_analysis(self, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list):
		pass

	def analyze(self, heuristic_function=None):
		print "In progress..."
		current_working_dir = os.path.dirname(os.path.abspath(__file__))
		project_working_dir = os.path.dirname(current_working_dir)
		all_map_files_dir = os.path.join(project_working_dir, self.all_map_directory_name)
		all_maps = [x[0] for x in os.walk(all_map_files_dir)]

		runtime_list = []
		pathlength_list = []
		num_nodes_traversed_list = []
		cost_incurred_list = []
		for map_dir in all_maps[1:]:
			map_dir_name = map_dir.replace(all_map_files_dir, "").replace("/", "").replace("\\","")
			print map_dir
			print [x[2] for x in os.walk(map_dir)]
			for map_name in [x[2] for x in os.walk(map_dir)][0]:
				print "map name ", map_name
				self.parse_map_file(map_dir_name, map_name)
				self.run_search_analysis(runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list, heuristic_function)
			print "Completed analysis for: ", map_dir_name
		print "Writing all data to file..."
		self.write_search_analysis(runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list)

		print "Completed analysis! You can find logs of the data in the Analysis folder.\n"

if __name__ == "__main__":
	visualizer = Visualizer()
	visualizer.init_default()

	map_group_name = raw_input("What is the name of the map group you are using?\n")
	map_file_name = raw_input("What is the name of the map file you wish to use?\n")
	if visualizer.parse_map_file(map_group_name, map_file_name):
		visualizer.display_map()
