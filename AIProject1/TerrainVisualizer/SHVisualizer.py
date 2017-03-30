import sys
sys.path.append("../AStar")
from SHStar import sequential_heuristic_astar
from Visualizer import Visualizer

class SHVisualizer(Visualizer):

  def __init__(self):
    super(SHVisualizer, self).__init__()

  def run_search(self):
    return sequential_heuristic_astar(self.map, 5, self.start_pos, self.end_pos, 1, 1)

if __name__ == "__main__":
  visualizer = SHVisualizer()
  visualizer.init_default()

  map_group_name = raw_input("What is the name of the map group you are using?\n")
  map_file_name = raw_input("What is the name of the map file you wish to use?\n")
  if visualizer.parse_map_file(map_group_name, map_file_name):
    visualizer.display_map()
