import sys, os
sys.path.append("../AStar")
from AStar import show_route, perform_analysis
from Visualizer import Visualizer

class ASVisualizer(Visualizer):

	def __init__(self):
		super(ASVisualizer, self).__init__()

	def run_search(self):
		return show_route(self.map, self.start_pos, self.end_pos, self.get_heuristic('manhattan distance'))

	def run_search_analysis(self, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list, heuristic_function):
		perform_analysis(self.map, self.start_pos, self.end_pos, heuristic_function, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list)

	def write_search_analysis(self, runtime_list, pathlength_list, num_nodes_traversed_list, cost_incurred_list):
		total_runtime = 0.0
		for i in range(len(runtime_list)):
			total_runtime += runtime_list[i]
		total_pathlength = 0.0
		for i in range(len(pathlength_list)):
			total_pathlength += pathlength_list[i]
		total_num_nodes_traversed = 0.0
		for i in range(len(num_nodes_traversed_list)):
			total_num_nodes_traversed += num_nodes_traversed_list[i]
		total_cost_incurred = 0.0
		for i in range(len(cost_incurred_list)):
			total_cost_incurred += cost_incurred_list[0]

		current_working_dir = os.path.dirname(os.path.abspath(__file__))
		project_working_dir = os.path.dirname(current_working_dir)
		analysis_files_folder = os.path.join(project_working_dir, "Analysis")
		analysis_file_path = os.path.join(analysis_files_folder, "AStar_"+self.heuristic_name)

		analysis_file = open(analysis_file_path, "w")
		analysis_file.write("Average Runtime:\n\t" + str(total_runtime/50) + "\n")
		analysis_file.write("Average Path Length:\n\t" + str(total_pathlength/50) + "\n")
		analysis_file.write("Average Nodes Traversed:\n\t" + str(total_num_nodes_traversed/50) + "\n")
		analysis_file.write("Average Cost:\n\t" + str(total_cost_incurred/50) + "\n")

		print "Average Runtime: " + str(total_runtime/50) + "\n"
		print "Average Path Length: " + str(total_pathlength/50) + "\n"
		print	"Average Nodes Traversed: " + str(total_num_nodes_traversed/50) + "\n"
		print "Average Cost: " + str(total_cost_incurred/50) + "\n"
		print "______________________________________"

if __name__ == "__main__":
	visualizer = ASVisualizer()
	visualizer.init_default()

	option = raw_input("Would you like to either display a search result or perform an analysis? (0 or 1)\n")

	if option == '0':
		map_group_name = raw_input("What is the name of the map group you would like to display?\n")
		map_file_name = raw_input("What is the name of the map file you wish to use?\n")
		if visualizer.parse_map_file(map_group_name, map_file_name):
				if visualizer.display_map():
					print "Path successfully generated"
				else:
					print "Could not generate path"
	elif option == '1':
		visualizer.analyze(visualizer.get_heuristic('manhattan distance'))
