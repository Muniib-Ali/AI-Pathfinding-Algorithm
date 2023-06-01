import pygame

cellWidth = 10
screenWidth = 1000
numberOfCells = int(screenWidth / cellWidth)
board = []
start = []
goal = []
searched = []
searchable = set()

class Cell:
    def __init__(self, colour, x,y):
        self.colour = colour
        self.x = x
        self.y = y

    def makeGoal(self):
        self.colour = "red"
    
    def clearColour(self):
        self.colour = "white"
    
    def makeStart(self):
        self.colour = "green"
    
    def makeWall(self):
        self.colour  = "black"

    def makeSearched(self):
        self.colour = "grey"

    def makeSearchable(self):
        self.colour = "yellow"
        
def fillGrid():
    for i in range(numberOfCells):
        board.append([])

        for j in range(numberOfCells):
            if i == 0 or  i == (numberOfCells) - 1 or j == 0 or j == (numberOfCells) - 1:
                board[i].append(Cell("black", 1 * i, 1 * j))

            else:
                board[i].append(Cell("white", 1 * i, 1 * j))

def drawGrid():
    frame.fill("white")
    
    for i in board:
        for j in i:
            pygame.draw.rect(frame, j.colour, (j.x * cellWidth , j.y * cellWidth, cellWidth, cellWidth))
    
    for i in range(numberOfCells):
        pygame.draw.line(frame, "black", (cellWidth * i,0), (cellWidth * i, screenWidth))
        pygame.draw.line(frame, "black", (0, cellWidth * i), (screenWidth, cellWidth * i))

    pygame.display.flip()

def placeCells():
    (mouseX, mouseY) = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] and mouseX >= 0 and mouseX < screenWidth and mouseY >= 0 and mouseY < screenWidth:
        mouseX = mouseX - (mouseX % cellWidth)
        mouseY = mouseY - (mouseY % cellWidth)
        cell = board[int(mouseX / cellWidth)][int(mouseY / cellWidth)]
        
        if not start and cell not in goal and cell.x != 0 and cell.x != (numberOfCells-1) and cell.y != 0  and cell.y != (numberOfCells-1): 
            cell.makeStart()
            start.append(cell)

        elif not goal and cell not in start and cell.x != 0 and cell.x != (numberOfCells-1) and cell.y != 0  and cell.y != (numberOfCells-1):
            cell.makeGoal()
            goal.append(cell)
        
        elif cell not in goal and cell not in start:
            cell.makeWall()

def deleteCells():
    (mouseX, mouseY) = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[2] and mouseX >= 0 and mouseX < screenWidth and mouseY >= 0 and mouseY < screenWidth: 
        mouseX = mouseX - (mouseX % cellWidth)
        mouseY = mouseY - (mouseY % cellWidth)

        cell = board[int(mouseX / cellWidth)][int(mouseY / cellWidth)]
        cell.clearColour()

        if cell in start:
            start.clear()
        elif cell in goal:
            goal.clear()

def getNeighbours(cell):
    neighbours = []
    found = False

    if cell.x > 0:
        neighbours.append(board[cell.x-1][cell.y])
    
    if cell.x < (numberOfCells - 1):
        neighbours.append(board[cell.x+1][cell.y])

    if cell.y < (numberOfCells - 1):
        neighbours.append(board[cell.x][cell.y+1])

    if cell.y > 0 :
        neighbours.append(board[cell.x][cell.y-1])
    
    for neighbour in neighbours:
        if neighbour not in searched and neighbour.colour != "black" and neighbour.colour != "red" and neighbour.colour != "green":
            searchable.add(neighbour)
            neighbour.makeSearchable()
        elif neighbour.colour == "red":
            found = True

    if found == True:
        searchable.clear()
        return   

def compare(cell1, cell2):

    target = goal[0]
    returnable = None

    comparable1 = abs(cell1.x - target.x) + abs(cell1.y - target.y)
    comparable2 = abs(cell2.x - target.x) + abs(cell2.y - target.y)

    if comparable1 > comparable2:
        returnable = cell2
    else:
        returnable = cell1
    return returnable

def getClosest():
    closestCell = None
    for cell in searchable:
        if closestCell == None:
            closestCell = cell
        else:  
            closestCell = compare(closestCell, cell)
    
    searchable.remove(closestCell)
    return closestCell

def search(cell):
    cell.makeSearched()
    searched.append(cell)

def bestFirstSearch():
    if pygame.key.get_pressed()[pygame.K_SPACE] and start and goal:
        getNeighbours(start[0])
        while len(searchable) != 0:
            running = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     running = False
                     pygame.quit()
            
            cell = getClosest()
            search(cell)
            getNeighbours(cell)
            drawGrid()
            pygame.time.wait(100)

pygame.init()
frame = pygame.display.set_mode((screenWidth, screenWidth))
pygame.display.set_caption('Pathfinding Algorithm')
running = True
fillGrid()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawGrid()
    placeCells()
    deleteCells()
    bestFirstSearch()