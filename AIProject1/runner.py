import pygame, sys
from pygame.locals import *
import os, sys
sys.path.append("/Users/DavidHuynh/Desktop/AIProject1/TerrainVisualizer")
from ASVisualizer import *
from ASWVisualizer import *
from UCSVisualizer import *


if __name__ == "__main__":
  	a = raw_input("Enter 0 (AStar), 1 (AStarW), 2 (UCS): ")
  	if a == '0':
  		os.system('python /Users/DavidHuynh/Desktop/AIProject1/TerrainVisualizer/ASVisualizer.py')
 	elif a == '1':
  		os.system('python /Users/DavidHuynh/Desktop/AIProject1/TerrainVisualizer/ASWVisualizer.py')
  	else:
   		os.system('python /Users/DavidHuynh/Desktop/AIProject1/TerrainVisualizer/UCSVisualizer.py')

