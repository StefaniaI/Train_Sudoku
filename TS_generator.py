import random

class CellRoom:

  def generateGame(self, n, m):
    ## Constants
    self.UNDEFINED = 0
    self.FROM_NOWHERE = 1
    self.FROM_NORTH = 2
    self.FROM_EAST = 3
    self.FROM_SOUTH = 4
    self.FROM_WEST = 5

    self.LEFT = 0
    self.RIGHT = 1

    self.GAME_WIDTH = m
    self.GAME_HEIGHT = n

    self.initGame()

    for i in range(100):
      self.permutate()

    ##self.logGameWithPath()
    ##self.logGameWithArrow()
    for i in range(50):
      self.start = self.moveExtremity(self.start)
    # Uncomment next 2 linesto also see the generated generated board
    # self.logGameWithPath()
    # self.logGameWithArrow()
    self.verifyGame()

  ## Print the map of the game on the standard output.
  ## Do not show the orientation.
  def logGameWithPath(self):
    print ('game width: ' + str(self.GAME_WIDTH))
    print ('game height: ' + str(self.GAME_HEIGHT))
    print ('Start [x=' + str(self.start[0]) + ', y=' + str(self.start[1]) + ']')

    gameText = ''

    for i in range(len(self.gameGrid)):
      for j in range(len(self.gameGrid[i])):
        if (self.gameGrid[i][j] == self.FROM_NORTH) or ((i > 0) and (self.gameGrid[i - 1][j] == self.FROM_SOUTH)):
          gameText = gameText + ' |'
        else:
          gameText = gameText + '  '
      gameText = gameText + ' \n'
      for j in range(len(self.gameGrid[i])):
        if (self.gameGrid[i][j] == self.FROM_WEST) or ((j > 0) and (self.gameGrid[i][j - 1] == self.FROM_EAST)):
          gameText = gameText + '-O'
        else:
          gameText = gameText + ' O'
      gameText = gameText + ' \n'

    for j in range(len(self.gameGrid[i])):
      gameText = gameText + '  '
    gameText = gameText + ' \n'
    
    # Uncomment this to see the game
    print (gameText)

  ## Print the map of the game on the standard output.
  ## It shows the orientation.
  def logGameWithArrow(self):
    gameText = ''

    for gameLine in self.gameGrid:
      for j in gameLine:
        if j == self.FROM_NOWHERE:
          gameText = gameText + 'X'
        elif j == self.FROM_NORTH:
          gameText = gameText + 'V'
        elif j == self.FROM_EAST:
          gameText = gameText + '('
        elif j == self.FROM_SOUTH:
          gameText = gameText + '^'
        elif j == self.FROM_WEST:
          gameText = gameText + ')'
      gameText = gameText + '\n'

    print (gameText)

  ## Generate a new map with an extremity (ex. start point) at another place.
  ## It receives and returns a valid map.
  def moveExtremity(self, extremity):
    ## Search the points.
    possibleNewOrigins = []
    if ((extremity[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[extremity[0] + 1][extremity[1]] != self.FROM_NORTH)):
      possibleNewOrigins.append(self.FROM_NORTH)
      besidePoint = [extremity[0] + 1, extremity[1]]
    elif ((extremity[1] > 0) and (self.gameGrid[extremity[0]][extremity[1] - 1] != self.FROM_EAST)):
      possibleNewOrigins.append(self.FROM_EAST)
      besidePoint = [extremity[0], extremity[1] - 1]
    elif ((extremity[0] > 0) and (self.gameGrid[extremity[0] - 1][extremity[1]] != self.FROM_SOUTH)):
      possibleNewOrigins.append(self.FROM_SOUTH)
      besidePoint = [extremity[0] - 1, extremity[1]]
    elif ((extremity[1] < self.GAME_WIDTH - 1) and (self.gameGrid[extremity[0]][extremity[1] + 1] != self.FROM_WEST)):
      possibleNewOrigins.append(self.FROM_WEST)
      besidePoint = [extremity[0], extremity[1] + 1]

    besidePointNewOrigin = possibleNewOrigins[random.randint(0, len(possibleNewOrigins) - 1)]

    if besidePointNewOrigin == self.FROM_NORTH:
      besidePoint = [extremity[0] + 1, extremity[1]]
    elif besidePointNewOrigin == self.FROM_EAST:
      besidePoint = [extremity[0], extremity[1] - 1]
    elif besidePointNewOrigin == self.FROM_SOUTH:
      besidePoint = [extremity[0] - 1, extremity[1]]
    elif besidePointNewOrigin == self.FROM_WEST:
      besidePoint = [extremity[0], extremity[1] + 1]

    ##print ('New start: [' + str(extremity[0]) + ', ' + str(extremity[1]) + ']')
    ##print ('besidePoint: [' + str(besidePoint[0]) + ', ' + str(besidePoint[1]) + ']')

    ## Search the new extremity
    if self.gameGrid[besidePoint[0]][besidePoint[1]] == self.FROM_NORTH:
      newExtremity = [besidePoint[0] - 1, besidePoint[1]]
    elif self.gameGrid[besidePoint[0]][besidePoint[1]] == self.FROM_EAST:
      newExtremity = [besidePoint[0], besidePoint[1] + 1]
    elif self.gameGrid[besidePoint[0]][besidePoint[1]] == self.FROM_SOUTH:
      newExtremity = [besidePoint[0] + 1, besidePoint[1]]
    elif self.gameGrid[besidePoint[0]][besidePoint[1]] == self.FROM_WEST:
      newExtremity = [besidePoint[0], besidePoint[1] - 1]

    ## Do the move.
    self.reversePath(extremity, newExtremity)

    self.gameGrid[besidePoint[0]][besidePoint[1]] = besidePointNewOrigin
    self.gameGrid[newExtremity[0]][newExtremity[1]] = self.FROM_NOWHERE
    ##print ('extremity: [' + str(newExtremity[0]) + ', ' + str(newExtremity[1]) + ']')

    return newExtremity

  ## Rewrite the path on the map as the end was the start and vice versa.
  ## The end becomes undefined.
  def reversePath(self, start, end):
    currentPoint = start
    ##print ('start: [' + str(currentPoint[0]) + ', ' + str(currentPoint[1]) + ']')
    ##print ('end: [' + str(end[0]) + ', ' + str(end[1]) + ']')
    while (currentPoint[0] != end[0]) or (currentPoint[1] != end[1]):
      ##print ('currentPoint: [' + str(currentPoint[0]) + ', ' + str(currentPoint[1]) + ']')
      ## We search the next point, not the point we just have reversed
      if (currentPoint[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[currentPoint[0] + 1][currentPoint[1]] == self.FROM_NORTH) and (self.gameGrid[currentPoint[0]][currentPoint[1]] != self.FROM_SOUTH):
        self.gameGrid[currentPoint[0]][currentPoint[1]] = self.FROM_SOUTH
        currentPoint[0] = currentPoint[0] + 1
      elif (currentPoint[1] > 0) and (self.gameGrid[currentPoint[0]][currentPoint[1] - 1] == self.FROM_EAST) and (self.gameGrid[currentPoint[0]][currentPoint[1]] != self.FROM_WEST):
        self.gameGrid[currentPoint[0]][currentPoint[1]] = self.FROM_WEST
        currentPoint[1] = currentPoint[1] - 1
      elif (currentPoint[0] > 0) and (self.gameGrid[currentPoint[0] - 1][currentPoint[1]] == self.FROM_SOUTH) and (self.gameGrid[currentPoint[0]][currentPoint[1]] != self.FROM_NORTH):
        self.gameGrid[currentPoint[0]][currentPoint[1]] = self.FROM_NORTH
        currentPoint[0] = currentPoint[0] - 1
      elif (currentPoint[1] < self.GAME_WIDTH - 1) and (self.gameGrid[currentPoint[0]][currentPoint[1] + 1] == self.FROM_WEST) and (self.gameGrid[currentPoint[0]][currentPoint[1]] != self.FROM_EAST):
        self.gameGrid[currentPoint[0]][currentPoint[1]] = self.FROM_EAST
        currentPoint[1] = currentPoint[1] + 1
    ##print ('reversePath: [' + str(currentPoint[0]) + ', ' + str(currentPoint[1]) + ']')
    self.gameGrid[currentPoint[0]][currentPoint[1]] = self.UNDEFINED

  ## Check that we go on every cell.
  def verifyGame(self):
    moveCount = 0
    currentPoint = [self.start[0], self.start[1]]

    isEnd = 0
    while (isEnd == 0):
      if (currentPoint[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[currentPoint[0] + 1][currentPoint[1]] == self.FROM_NORTH):
        currentPoint[0] = currentPoint[0] + 1
      elif (currentPoint[1] > 0) and (self.gameGrid[currentPoint[0]][currentPoint[1] - 1] == self.FROM_EAST):
        currentPoint[1] = currentPoint[1] - 1
      elif (currentPoint[0] > 0) and (self.gameGrid[currentPoint[0] - 1][currentPoint[1]] == self.FROM_SOUTH):
        currentPoint[0] = currentPoint[0] - 1
      elif (currentPoint[1] < self.GAME_WIDTH - 1) and (self.gameGrid[currentPoint[0]][currentPoint[1] + 1] == self.FROM_WEST):
        currentPoint[1] = currentPoint[1] + 1
      else:
        isEnd = 1

      if isEnd == 0:
        moveCount = moveCount + 1
        
  ## Return path - added by Stefania
  def path(self):
    moveCount = 0
    currentPoint = [self.start[0], self.start[1]]

    isEnd = 0
    game_path = []
    while (isEnd == 0):
      c = (currentPoint[0], currentPoint[1])
      game_path.append(c)
      if (currentPoint[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[currentPoint[0] + 1][currentPoint[1]] == self.FROM_NORTH):
        currentPoint[0] = currentPoint[0] + 1
      elif (currentPoint[1] > 0) and (self.gameGrid[currentPoint[0]][currentPoint[1] - 1] == self.FROM_EAST):
        currentPoint[1] = currentPoint[1] - 1
      elif (currentPoint[0] > 0) and (self.gameGrid[currentPoint[0] - 1][currentPoint[1]] == self.FROM_SOUTH):
        currentPoint[0] = currentPoint[0] - 1
      elif (currentPoint[1] < self.GAME_WIDTH - 1) and (self.gameGrid[currentPoint[0]][currentPoint[1] + 1] == self.FROM_WEST):
        currentPoint[1] = currentPoint[1] + 1
      else:
        isEnd = 1

      if isEnd == 0:
        moveCount = moveCount + 1
      
    return game_path

    ## The number of moves should equal to the size of the map minus one cell because we don't arrive on the start
    if moveCount == ((self.GAME_HEIGHT * self.GAME_WIDTH) - 1):
      print ('OK')
    else:
      print ('ko!!!')

  ## Fill the map with void data.
  def initGame(self):
    self.gameGrid = []
    for i in range(self.GAME_HEIGHT):
      gameLine = []
      for j in range(self.GAME_WIDTH):
        gameLine.append(self.UNDEFINED)

      self.gameGrid.append(gameLine)

    self.initComplexMap()

  ## Create a valid simple map.
  ## It uses a complex algorithm.
  def initComplexMap(self):
    startPoint = random.randint(0, 3)
    if startPoint == 0:
      self.start = [0, 0]
    elif startPoint == 1:
      self.start = [0, self.GAME_WIDTH - 1]
    elif startPoint == 2:
      self.start = [self.GAME_HEIGHT - 1, 0]
    elif startPoint == 3:
      self.start = [self.GAME_HEIGHT - 1, self.GAME_WIDTH - 1]

    self.gameGrid[self.start[0]][self.start[1]] = self.FROM_NOWHERE
    currentPoint = [self.start[0], self.start[1]]

    while ((0 < currentPoint[0]) and (self.gameGrid[currentPoint[0] - 1][currentPoint[1]] == self.UNDEFINED)) or ((currentPoint[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[currentPoint[0] + 1][currentPoint[1]] == self.UNDEFINED)) or ((0 < currentPoint[1]) and (self.gameGrid[currentPoint[0]][currentPoint[1] - 1] == self.UNDEFINED)) or ((currentPoint[1] < self.GAME_WIDTH - 1) and (self.gameGrid[currentPoint[0]][currentPoint[1] + 1] == self.UNDEFINED)):
      possibilities = []
      if ((0 < currentPoint[0]) and (self.gameGrid[currentPoint[0] - 1][currentPoint[1]] == self.UNDEFINED)) and (((0 == currentPoint[1]) or (self.gameGrid[currentPoint[0] - 1][currentPoint[1] - 1] != self.UNDEFINED)) or ((currentPoint[1] == self.GAME_WIDTH - 1) or (self.gameGrid[currentPoint[0] - 1][currentPoint[1] + 1] != self.UNDEFINED))):
        possibilities.append([currentPoint[0] - 1, currentPoint[1], self.FROM_SOUTH])

      if ((currentPoint[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[currentPoint[0] + 1][currentPoint[1]] == self.UNDEFINED)) and (((0 == currentPoint[1]) or (self.gameGrid[currentPoint[0] + 1][currentPoint[1] - 1] != self.UNDEFINED)) or ((currentPoint[1] == self.GAME_WIDTH - 1) or (self.gameGrid[currentPoint[0] + 1][currentPoint[1] + 1] != self.UNDEFINED))):
        possibilities.append([currentPoint[0] + 1, currentPoint[1], self.FROM_NORTH])

      if ((0 < currentPoint[1]) and (self.gameGrid[currentPoint[0]][currentPoint[1] - 1] == self.UNDEFINED)) and (((0 == currentPoint[0]) or (self.gameGrid[currentPoint[0] - 1][currentPoint[1] - 1] != self.UNDEFINED)) or ((currentPoint[0] == self.GAME_HEIGHT - 1) or (self.gameGrid[currentPoint[0] + 1][currentPoint[1] - 1] != self.UNDEFINED))):
        possibilities.append([currentPoint[0], currentPoint[1] - 1, self.FROM_EAST])

      if ((currentPoint[1] < self.GAME_WIDTH - 1) and (self.gameGrid[currentPoint[0]][currentPoint[1] + 1] == self.UNDEFINED)) and (((0 == currentPoint[0]) or (self.gameGrid[currentPoint[0] - 1][currentPoint[1] + 1] != self.UNDEFINED)) or ((currentPoint[0] == self.GAME_HEIGHT - 1) or (self.gameGrid[currentPoint[0] + 1][currentPoint[1] + 1] != self.UNDEFINED))):
        possibilities.append([currentPoint[0], currentPoint[1] + 1, self.FROM_WEST])

      possibility = possibilities.pop(random.randint(0, len(possibilities) - 1))
      currentPoint = [possibility[0], possibility[1]]
      self.gameGrid[possibility[0]][possibility[1]] = possibility[2]

  ## Create a valid simple map.
  ## It uses a basic algorithm.
  def initSimpleMap(self):
    direction = self.RIGHT

    if random.randint(0, 1) == 0:
      for i in range(self.GAME_HEIGHT):
        if direction == self.RIGHT:
          self.gameGrid[i][0] = self.FROM_NORTH
          for j in range(1, self.GAME_WIDTH):
            self.gameGrid[i][j] = self.FROM_WEST
          direction = self.LEFT
        else:
          for j in range(self.GAME_WIDTH - 1):
            self.gameGrid[i][j] = self.FROM_EAST
          self.gameGrid[i][self.GAME_WIDTH - 1] = self.FROM_NORTH
          direction = self.RIGHT

        self.gameGrid.append(gameLine)

      self.gameGrid[0][0] = self.FROM_NOWHERE
    else:
      for j in range(self.GAME_WIDTH):
        if direction == self.RIGHT:
          self.gameGrid[0][j] = self.FROM_WEST
          for i in range(1, self.GAME_HEIGHT):
            self.gameGrid[i][j] = self.FROM_NORTH
          direction = self.LEFT
        else:
          for i in range(self.GAME_HEIGHT - 1):
            self.gameGrid[i][j] = self.FROM_SOUTH
          self.gameGrid[self.GAME_HEIGHT - 1][j] = self.FROM_WEST
          direction = self.RIGHT

      self.gameGrid[0][0] = self.FROM_NOWHERE

  ## Search all the possible permutations.
  ## It doesn't affect the map.
  def listPermutation(self):
    self.permutableZones = []
    for i in range(self.GAME_HEIGHT - 1):
      for j in range(self.GAME_WIDTH - 1):
        if (self.gameGrid[i + 1][j] == self.FROM_NORTH) and (self.gameGrid[i][j + 1] == self.FROM_SOUTH):
          self.permutableZones.append([[i + 1, j], [i, j + 1]])
        elif (self.gameGrid[i][j] == self.FROM_SOUTH) and (self.gameGrid[i + 1][j + 1] == self.FROM_NORTH):
          self.permutableZones.append([[i, j], [i + 1, j + 1]])
        elif (self.gameGrid[i][j] == self.FROM_EAST) and (self.gameGrid[i + 1][j + 1] == self.FROM_WEST):
          self.permutableZones.append([[i, j], [i + 1, j + 1]])
        elif (self.gameGrid[i][j + 1] == self.FROM_WEST) and (self.gameGrid[i + 1][j] == self.FROM_EAST):
          self.permutableZones.append([[i, j + 1], [i + 1, j]])

  ## Permutate the connection of path.
  ## It receives and returns a valid map.
  def permutate(self):
    self.listPermutation()

    if len(self.permutableZones) > 0:
      permutation = self.permutableZones.pop(random.randint(0, len(self.permutableZones) - 1))
      start = permutation[0]
      end = permutation[1]
      ##print ('Entry of the loop: (' + str(start[0]) + ', ' + str(start[1]) + ')')
      ##print ('Exit of the loop: (' + str(end[0]) + ', ' + str(end[1]) + ')')
      if self.isLoop(end, start):
        self.findPermutation(start, end)
      else:
        end = permutation[0]
        start = permutation[1]
        ## Assertion
        if not self.isLoop(end, start):
          print ('Wrong!')
        self.findPermutation(start, end)

  ## It doesn't affect the map.
  def isInLoop(self, searchedPoint):
    found = False
    for point in self.currentLoop:
      if (searchedPoint[0] == point[0]) and (searchedPoint[1] == point[1]):
        found = True

    return found

  ## It doesn't affect the map.
  def isLoop(self, originalPoint, destination):
    self.currentLoop = []

    point = []
    point.append(originalPoint[0])
    point.append(originalPoint[1])
    self.currentLoop.append([originalPoint[0], originalPoint[1]])
    while ((point[0] != destination[0]) or (point[1] != destination[1])) and (self.gameGrid[point[0]][point[1]] != self.FROM_NOWHERE):
      ##print ('Loop point: (' + str(point[0]) + ', ' + str(point[1]) + ')')
      newY = point[0]
      newX = point[1]
      if self.gameGrid[point[0]][point[1]] == self.FROM_SOUTH:
        newY = point[0] + 1
      elif self.gameGrid[point[0]][point[1]] == self.FROM_NORTH:
        newY = point[0] - 1
      elif self.gameGrid[point[0]][point[1]] == self.FROM_WEST:
        newX = point[1] - 1
      elif self.gameGrid[point[0]][point[1]] == self.FROM_EAST:
        newX = point[1] + 1
      point[0] = newY
      point[1] = newX
      self.currentLoop.append([newY, newX])

    return ((point[0] == destination[0]) and (point[1] == destination[1]))

  ## Permutate the connections of path.
  ## It receives and returns a valid map.
  def findPermutation(self, start, end):
    self.findIntersections()
    if len(self.intersections) > 0:
      self.modifyIntersection(start, end)

  ## Permutate the connections of path.
  ## It doesn't affect the map.
  def findIntersections(self):
    self.intersections = []
    for i in range(1, len(self.currentLoop) - 1):
      point = self.currentLoop[i]
      if self.gameGrid[point[0]][point[1]] == self.FROM_NORTH:
        if (0 < point[1]) and (self.gameGrid[point[0] - 1][point[1] - 1] == self.FROM_SOUTH) and not self.isInLoop([point[0] - 1, point[1] - 1]):
          self.intersections.append([[point[0], point[1]], [point[0] - 1, point[1] - 1]])
        elif (point[1] < self.GAME_WIDTH - 1) and (self.gameGrid[point[0] - 1][point[1] + 1] == self.FROM_SOUTH) and not self.isInLoop([point[0] - 1, point[1] + 1]):
          self.intersections.append([[point[0], point[1]], [point[0] - 1, point[1] + 1]])

      elif self.gameGrid[point[0]][point[1]] == self.FROM_SOUTH:
        if (0 < point[1]) and (self.gameGrid[point[0] + 1][point[1] - 1] == self.FROM_NORTH) and not self.isInLoop([point[0] + 1, point[1] - 1]):
          self.intersections.append([[point[0], point[1]], [point[0] + 1, point[1] - 1]])
        elif (point[1] < self.GAME_WIDTH - 1) and (self.gameGrid[point[0] + 1][point[1] + 1] == self.FROM_NORTH) and not self.isInLoop([point[0] + 1, point[1] + 1]):
          self.intersections.append([[point[0], point[1]], [point[0] + 1, point[1] + 1]])

      elif self.gameGrid[point[0]][point[1]] == self.FROM_WEST:
        if (0 < point[0]) and (self.gameGrid[point[0] - 1][point[1] - 1] == self.FROM_EAST) and not self.isInLoop([point[0] - 1, point[1] - 1]):
          self.intersections.append([[point[0], point[1]], [point[0] - 1, point[1] - 1]])
        elif (point[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[point[0] + 1][point[1] - 1] == self.FROM_EAST) and not self.isInLoop([point[0] + 1, point[1] - 1]):
          self.intersections.append([[point[0], point[1]], [point[0] + 1, point[1] - 1]])

      elif self.gameGrid[point[0]][point[1]] == self.FROM_EAST:
        if (0 < point[0]) and (self.gameGrid[point[0] - 1][point[1] + 1] == self.FROM_WEST) and not self.isInLoop([point[0] - 1, point[1] + 1]):
          self.intersections.append([[point[0], point[1]], [point[0] - 1, point[1] + 1]])
        elif (point[0] < self.GAME_HEIGHT - 1) and (self.gameGrid[point[0] + 1][point[1] + 1] == self.FROM_WEST) and not self.isInLoop([point[0] + 1, point[1] + 1]):
          self.intersections.append([[point[0], point[1]], [point[0] + 1, point[1] + 1]])

  ## Permutate the connections of path.
  ## It receives and returns a valid map.
  def modifyIntersection(self, start, end):
    ##self.logGameWithPath()
    ##self.printGameOld()
    intersection = self.intersections[random.randint(0, len(self.intersections) - 1)]
    ## Disconnect the loop
    self.modifyPath([start, end])
    ## Reconnect the loop
    self.modifyPath(intersection)

  ## Change the connections on the map.
  def modifyPath(self, intersection):
    ##print ('modifyPath: (' + str(intersection[0][0]) + ', ' + str(intersection[0][1]) + ') with (' + str(intersection[1][0]) + ', ' + str(intersection[1][1]) + ')')
    firstPoint = self.gameGrid[intersection[0][0]][intersection[0][1]]
    secondPoint = self.gameGrid[intersection[1][0]][intersection[1][1]]

    if (self.gameGrid[intersection[0][0]][intersection[0][1]] == self.FROM_NORTH) or (self.gameGrid[intersection[0][0]][intersection[0][1]] == self.FROM_SOUTH):
      if (intersection[0][1] < intersection[1][1]):
        firstPoint = self.FROM_EAST
        secondPoint = self.FROM_WEST
      else:
        firstPoint = self.FROM_WEST
        secondPoint = self.FROM_EAST
    if (self.gameGrid[intersection[0][0]][intersection[0][1]] == self.FROM_EAST) or (self.gameGrid[intersection[0][0]][intersection[0][1]] == self.FROM_WEST):
      if (intersection[0][0] < intersection[1][0]):
        firstPoint = self.FROM_SOUTH
        secondPoint = self.FROM_NORTH
      else:
        firstPoint = self.FROM_NORTH
        secondPoint = self.FROM_SOUTH

    self.gameGrid[intersection[0][0]][intersection[0][1]] = firstPoint
    self.gameGrid[intersection[1][0]][intersection[1][1]] = secondPoint

cellRoom = CellRoom()

# From here on, only Stefania's adds
# This generates a Train Sudoku
def sudo_train_gen(game_sze):
  '''This generates a random game of the given size'''
  
  n, m, k = game_sze
  
  cellRoom.generateGame(n, m)
  sol = cellRoom.path()
  
  # Take k random stions
  index_stations = random.sample(range(1, n*m-1), k-2)
  index_stations.append(0)
  index_stations.append(n*m-1)
  index_stations.sort()
  
  game = [n, m, k]
  for i in range(k):
    game.append(sol[index_stations[i]])
  
  return game

def st_dataset(n, m, no_tests):
  '''Generates a dataset for boards of syze n by m, with test_no may examples 
  for every k between 2 and n*m'''
  
  name = 'dataset_' + str(n) + 'by' + str(m) + '_' + str(no_tests) +'.txt'
  with open(name, 'w') as f:
    for k in range(2, n*m + 1):
      game_sze = (n, m, k)
      for i in range(no_tests):
        f.write(str(sudo_train_gen(game_sze))[1:-1] + '\n')

def st_dataset_9by9(no_tests):
  '''Generates a dataset for boards of syze 9 by 9, with test_no may examples 
  for every k between 2 and 29, and test_no/10 for k between 30 and n*m'''
  
  n = 9
  m = 9
  name = 'dataset_' + str(n) + 'by' + str(m) + '_' + str(no_tests) +'.txt'
  with open(name, 'w') as f:
    for k in range(2, 15):
      game_sze = (n, m, k)
      for i in range(no_tests):
        f.write(str(sudo_train_gen(game_sze))[1:-1] + '\n')
    
    for k in range(15, 30):
      game_sze = (n, m, k)
      for i in range(no_tests/4):
        f.write(str(sudo_train_gen(game_sze))[1:-1] + '\n')
    
    for k in range(30, n*m + 1):
      game_sze = (n, m, k)
      for i in range(no_tests/20):
        f.write(str(sudo_train_gen(game_sze))[1:-1] + '\n')