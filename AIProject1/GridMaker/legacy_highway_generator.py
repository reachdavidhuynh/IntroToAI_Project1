  valid = False
        completed = False
        while not valid:
          temp_highway = []

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

          highway_start_pos_terrain = getattr(grid[highway_start_pos[0]][highway_start_pos[1]], 'terrain_type')

          #print "highway strt pos", highway_start_pos

          if(highway_start_pos_terrain == '0'):
            continue
          elif(len(highways) == 0):
            valid = True
          else:
            for highway in highways:
              if highway_start_pos == highway[0]:
                valid = False
                break
              else:
                valid = True
          if not valid:
            continue
          else:
            temp_highway.append(highway_start_pos)

          #print temp_highway
          highway_current_pos = highway_start_pos

          temp_highway_start = []

          for i in range(0, highway_segment_length-1):
            highway_current_pos = (highway_current_pos[0]+highway_direction[0], highway_current_pos[1]+highway_direction[1])
            if(highway_current_pos[0] > 0) and (highway_current_pos[1] > 0) and (highway_current_pos[0] < total_columns-1) and (highway_current_pos[1] < total_rows-1) and (temp_highway_start < highway_total_length):
              current_cell_terrain = getattr(grid[highway_current_pos[0]][highway_current_pos[1]], 'terrain_type')
              if(current_cell_terrain == '0'):
                valid = False
                break
              else:
                for highway in highways:
                  if highway_current_pos in highway:
                    valid = False
                    break
                  else:
                    valid = True
                if valid:
                  temp_highway_start.append(highway_current_pos)
                else:
                  break
            else:
              temp_highway_start.append(highway_current_pos)
              valid = True
              completed = True
              print "hits", "\nhighway current_pos", highway_current_pos, "\nhighway direction", highway_direction, "\nrandom cell", random_cell
              break

          if completed:
            highways.append(temp_highway_start)
            break
          if not valid:
            continue

          #print "temp_highway p1: ", temp_highway, "\ntemp_highway size", len(temp_highway)

          temp_highway_turn = []
          length_reached = False
          old_highway_current_pos = highway_current_pos
          old_highway_direction = highway_direction
          attempts = 100
          while attempts > 0:
            temp_turn = []

            make_turn = randint(0, 9)
            while make_turn >= 7:
              make_turn = randint(0, 9)

            if(make_turn > 5) and (make_turn < 8):
              new_highway_direction = randint(0, 1)
              if(new_highway_direction == 0):
                if(highway_direction == (0, -1)):
                  highway_direction = (-1, 0)
                elif(highway_direction == (0, 1)):
                  highway_direction = (1, 0)
                elif(highway_direction == (1, 0)):
                  highway_direction = (0, -1)
                elif(highway_direction == (-1, 0)):
                  highway_direction = (0, 1)
              else:
                if(highway_direction == (0, -1)):
                  highway_direction = (1, 0)
                elif(highway_direction == (0, 1)):
                  highway_direction = (-1, 0)
                elif(highway_direction == (1, 0)):
                  highway_direction = (0, 1)
                elif(highway_direction == (-1, 0)):
                  highway_direction = (0, -1)

            #print "turn 1 ", make_turn, "\nturn 2", highway_direction

            for i in range(0, highway_segment_length):
              highway_current_pos = (highway_current_pos[0]+highway_direction[0], highway_current_pos[1]+highway_direction[1])
              if(highway_current_pos[0] > 0) and (highway_current_pos[1] > 0) and (highway_current_pos[0] < total_columns-1) and (highway_current_pos[1] < total_rows-1):
                current_cell_terrain = getattr(grid[highway_current_pos[0]][highway_current_pos[1]], 'terrain_type')
                if(current_cell_terrain == '0'):
                  valid = False
                  break
                else:
                  for highway in highways:
                    if highway_current_pos in highway:
                      valid = False
                      break
                    else:
                      valid = True
                  if not valid:
                    break
                  if highway_current_pos in temp_highway_turn:
                    valid = False
                    break
                  temp_turn.append(highway_current_pos)
              else:
                temp_turn.append(highway_current_pos)
                valid = True
                completed = True
                break
            if not valid:
              attempts-=1
              highway_current_pos = old_highway_current_pos
              highway_direction = old_highway_direction
              continue
            else:
              if completed:
                if(len(temp_highway_turn) + len(temp_turn) + len(temp_highway_start) < highway_total_length):
                  valid = False
                  completed = False
                  attempts-=1
                  continue
                for cell in temp_turn:
                  temp_highway_turn.append(cell)
                length_reached = True
                break
              elif valid:
                attempts = 100
                old_highway_current_pos = highway_current_pos
                old_highway_direction = highway_direction
                for cell in temp_turn:
                  temp_highway_turn.append(cell)
                continue

          if completed and length_reached:
            for cell in temp_highway_start:
              temp_highway.append(cell)
            for cell in temp_highway_turn:
              temp_highway.append(cell)

            highways.append(temp_highway)
            break
          else:
            valid = False
            completed = False
            continue

      for highway in highways:
        print highway
        for cell in highway:
          cell_terrain = getattr(grid[cell[0]][cell[1]], 'terrain_type')
          if(cell_terrain == '1'):
            setattr(grid[cell[0]][cell[1]], 'terrain_type', 'a')
          elif(cell_terrain == '2'):
            setattr(grid[cell[0]][cell[1]], 'terrain_type', 'b')
          else:
            print "error ", cell, "terrain type ", cell_terrain
