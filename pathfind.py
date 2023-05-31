import pygame

cellWidth = 10
screenWidth = 1000
numberOfCells = int(screenWidth / cellWidth)
board = []
start = []
goal = []

class Cell:
    def __init__(self, colour, x,y):
        self.colour = colour
        self.x = x
        self.y = y

    def makeGoal(self):
        self.colour = "red"
    
    def clearColor(self):
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
    if pygame.mouse.get_pressed()[0]:

        (mouseX, mouseY) = pygame.mouse.get_pos() 
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