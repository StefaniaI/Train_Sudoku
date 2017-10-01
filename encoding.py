# This gives the encoding of a Train Sudoku problem into  DIMACS cnf format.
# It also provides a decoding, so given the list with the truth values of the
#   variables, it returnsthe solution ofthe given problem.

import pycosat
import pandas as pd

def cell_to_vertex (game_sze, cell):
  '''Given the size of the board and a cell's row and culumn coordinates it 
  returns the corresponding vertex number'''
  
  m = game_sze[1]
  row = cell[0]
  column = cell[1]
  return (m * row + column)
  
def vertex_to_cell (game_sze, vtx):
  '''Given the size of the board and the vertex it returns the cell's
  coordinates'''
  
  m = game_sze[1]
  return (vtx / m, vtx % m)

def vertex_nbhs (game_sze, vtx):
  '''For a given grid size, and vertex, returns the list of neighbours of that
  vertex'''
  
  (r, c) = vertex_to_cell(game_sze, vtx)
  nbhs = []
  n, m, k = game_sze
  
  # Check if each candidate neighbour is in the grid, if yes add it to nbhs
  candidats = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
  for c in candidats:
    if c[0] >=  0 and c[0] < n and c[1] >=  0 and c[1] < m:
      nbhs.append(cell_to_vertex(game_sze, c))
  
  return nbhs

def exactly_before (game_sze, vtx1, vtx2):
  '''Given the sizes of the grid, and the two vertices it returns the encoding 
  of x_(vtx1,vtx2), i.e. the variable saying if the edge (vtx1, vtx2) is in the 
  path
  WARNING: vtx1 and vtx2 must correspond to adjacent cells!'''
  
  n, m, k = game_sze
  
  if vtx1 not in vertex_nbhs(game_sze, vtx2):
    raise ValueError('The two vertices are not adjacent')
  else:
    if vtx2 == vtx1 - m:
      dirn = 0
    elif vtx2 == vtx1 + 1:
      dirn = 1
    elif vtx2 == vtx1 + m:
      dirn = 2
    else:
      dirn = 3
    
    x = 1 + 4 * vtx1 + dirn
      
    return x
    
def is_exactly_before (game_sze, var):
  '''Given the sizes of the grid, and the value of some x_(vtx1,vtx2) it returns
  the values of vtx1 and vtx2'''
  
  n, m, k = game_sze
  
  vtx1 = int((var - 1) /  4)
  dirn = (var - 1) % 4
  if dirn == 0:
    vtx2 = vtx1 - m
  elif dirn == 1:
    vtx2 = vtx1 + 1
  elif dirn == 2:
    vtx2 = vtx1 + m
  else:
    vtx2 = vtx1 - 1
  
  return (vtx1, vtx2)

def before (game_sze, vtx1, vtx2):
  '''Given the sizes of the grid, and the two vertices it returns the encoding 
  of y_(vtx1,vtx2), i.e. the variable saying if vtx1 appears before vtx2 in the 
  path
  WARNING: vtx1 and vtx2 must correspond to adjacent cells!'''
  
  n, m, k = game_sze
  
  return 1 + 4 * n * m + vtx1 * n * m + vtx2

def cnf_encoding (game):
  '''This returns the cnf encoding for a given game.
  The format of the game is expected to be n, m, k, followed by k pairs
  representing the coordinates of the k stations in order'''
  
  n = game[0]
  m = game[1]
  k = game[2]
  game_sze = (n, m, k)
  
  stations = game[3:]
  vtx_stations =[]
  for stn in stations:
    vtx_stations.append(cell_to_vertex(game_sze, stn))
  end_stations = [vtx_stations[0], vtx_stations[-1]]
  start = end_stations[0]
  end = end_stations[1]
  
  cnf = []
  
  # Each cell, besides last station, has exactly one neighbouring cell 
  # exactly after the cell, in the Hamiltonian path
  for vtx in range(n*m):
    nbhs = vertex_nbhs(game_sze, vtx)
    
    if vtx != end:
      # Each non-end station has one successor in the path
      clause = []
      
      for nbh in nbhs:
        clause.append(exactly_before(game_sze, vtx, nbh))
      
      cnf.append(clause)
      
      # Each non-end station has exactly one successor in the path
      for nbh1 in nbhs:
        for nbh2 in nbhs:
          if nbh1 < nbh2:
            clause = [-exactly_before(game_sze, vtx, nbh1),
            -exactly_before(game_sze, vtx, nbh2)]
            cnf.append(clause)
      
    else:
      # The last station has no successor
      for nbh in nbhs:
        cnf.append([-exactly_before(game_sze, vtx, nbh)])
  
  # Each cell A, besides first station, has exactly one neighbouring cell 
  # exactly before A, in the Hamiltonian path
  for vtx in range(n*m):
    nbhs = vertex_nbhs(game_sze, vtx)
    
    if vtx != start:
      # Each non-start station has one predecessor in the path
      clause = []
      
      for nbh in nbhs:
        clause.append(exactly_before(game_sze, nbh, vtx))
      
      cnf.append(clause)
      
      # Each non-start station has exactly one predecessor in the path
      for nbh1 in nbhs:
        for nbh2 in nbhs:
          if nbh1 < nbh2:
            clause = [-exactly_before(game_sze, nbh1, vtx),
            -exactly_before(game_sze, nbh2, vtx)]
            cnf.append(clause)
      
    else:
      # The first station has no predecessor
      for nbh in nbhs:
        cnf.append([-exactly_before(game_sze, nbh, vtx)])
  
  # If A is exactly before B, then A is before B
  for vtx in range(n*m):
    nbhs = vertex_nbhs(game_sze, vtx)
    
    for nbh in nbhs:
      clause = [-exactly_before(game_sze, vtx, nbh), before(game_sze, vtx, nbh)]
      cnf.append(clause)
  
  # Before is a transitive relation
  for vtx1 in range(n*m):
    for vtx2 in range(n*m):
      if vtx1 != vtx2:
        for vtx3 in range(n*m):
          if vtx3 != vtx2:
            clause = [-before(game_sze, vtx1, vtx2), 
            -before(game_sze, vtx2, vtx3), before(game_sze, vtx1, vtx3)]
            cnf.append(clause)
  
  # No cycles, i.e. if A cannot be before itself
  for vtx in range(n*m):
    cnf.append([-before(game_sze, vtx, vtx)])
  
  # Start station is before any other vertex
  for vtx in range(n*m):
    if vtx != start:
      cnf.append([before(game_sze, start, vtx)])
  
  # End station is after any other vertex
  for vtx in range(n*m):
    if vtx != end:
      cnf.append([before(game_sze, vtx, end)])
  
  # Stations are in the right order
  for i in range(1, k-2):
    cnf.append([before(game_sze, vtx_stations[i], vtx_stations[i+1])])
  
  return cnf

def solved  (game):
  cnf = cnf_encoding(game)
  sol = pycosat.solve(cnf)
  
  n = game[0]
  m = game[1]
  k = game[2]
  game_sze = (n, m, k)
  
  solved_table = []
  for i in range(n):
    row = []
    for j in range(m):
      row.append(0)
    solved_table.append(row)
  
  cur_vtx = cell_to_vertex(game_sze, game[3])
  row, column = vertex_to_cell(game_sze, cur_vtx)
  solved_table[row][column] = 1
  for i in range(n*m-1):
    nbhs = vertex_nbhs(game_sze, cur_vtx)
    for nbh in nbhs:
      if sol[exactly_before(game_sze, cur_vtx, nbh)-1]>0:
        nbh_r, nbh_c = vertex_to_cell(game_sze, nbh)
        solved_table[nbh_r][nbh_c] =  i+2
        next_vtx = nbh
    cur_vtx = next_vtx
  
  return solved_table

def unsolved (game):
  n = game[0]
  m = game[1]
  k = game[2]
  game_sze = (n, m, k)
  
  unsolved_table = []
  for i in range(n):
    row = []
    for j in range(m):
      row.append(0)
    unsolved_table.append(row)
  
  for i in range(3, k+3):
    unsolved_table[game[i][0]][game[i][1]] = i - 2
  
  return unsolved_table

def solve_and_print (game):
  print pd.DataFrame(unsolved(game))
  print pd.DataFrame(solved(game))

# This is for testing purposes only
# Call example_solve to se the output for 4 distinct examples
def example_game_1 ():
  return [5, 5, 6, (3, 1), (2, 4), (0, 4), (4, 0), (3, 3), (2, 2)]

def example_game_2 ():
  return [2, 2, 4, (0, 0), (1, 0), (1, 1), (0, 1)]

def example_game_3 ():
  return [2, 3, 3, (0, 0), (1, 1), (1, 2)]

def example_game_4():
  return [13, 13, 2, (10, 10), (10, 4)]

def example_solve ():
  solve_and_print(example_game_1())
  solve_and_print(example_game_2())
  solve_and_print(example_game_3())
  solve_and_print(example_game_4())