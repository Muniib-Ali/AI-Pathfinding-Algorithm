import pygame
from collections import deque

pygame.font.init()
cellWidth = 10
screenWidth = 1000
numberOfCells = int(screenWidth / cellWidth)
cyan = (0, 255, 255)
homePageColour = (0,0,0)
font =  pygame.font.SysFont(None, 40)
breadthSearch = False
bestSearch = False
board = []
start = []
goal = []
searched = []
searchable = []
bfsSearchable = deque()

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

def drawButtonBorder(width, height, y, search):
    pygame.draw.rect(frame, cyan, (screenWidth/2 - (width/2), y - (height/2), width, height))
    pygame.draw.rect(frame, "black", (screenWidth/2 - (width/2) + 10, y - (height/2) + 5, width - 20, height - 10))

    (mouseX, mouseY) = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and mouseX > screenWidth/2 - (width/2) and mouseX < screenWidth/2 + (width/2) and mouseY >  y - (height/2) and mouseY < y + (height/2):
        if search == "breadthSearch":
            global breadthSearch
            breadthSearch = True
        elif search == "bestSearch":
            global bestSearch
            bestSearch = True

def drawBorder(width, height, y, search):
    pygame.draw.rect(frame, cyan, (screenWidth/2 - (width/2), y - (height/2), width, height))
    pygame.draw.rect(frame, "black", (screenWidth/2 - (width/2) + 10, y - (height/2) + 5, width - 20, height - 10))

def drawText(text, height, colour):
    
    text = font.render(text, True, colour)
    text_rect = text.get_rect(center = (screenWidth/2, height))
    frame.blit(text, text_rect)
    

def drawHomepage():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    frame.fill(homePageColour)

    drawButtonBorder(500, 40, 200, "breadthSearch")
    drawText("Run Breadth First Search", 200, cyan)

    drawButtonBorder(500, 40, 300, "bestSearch")
    drawText("Run Best First Search", 300, cyan)

    drawText("Controls:", 400, "red")

    drawText("Left Click: Place", 450, "red")
    drawText("Right Click: Delete", 500, "red")
    drawText("Space Bar: Run Algorithm", 550, "red")



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
        if neighbour not in searched and neighbour not in bfsSearchable and neighbour.colour != "black" and neighbour.colour != "red" and neighbour.colour != "green":
            searchable.append(neighbour)
            bfsSearchable.append(neighbour)
            neighbour.makeSearchable()
        elif neighbour.colour == "red":
            found = True

    if found == True:
        searchable.clear()
        bfsSearchable.clear()

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
            
            cell = getClosest()
            search(cell)
            getNeighbours(cell)
            drawGrid()

def breadthFirstSearch():
    if pygame.key.get_pressed()[pygame.K_SPACE] and start and goal:
        getNeighbours(start[0])
        while len(bfsSearchable) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
            
            cell = bfsSearchable.popleft()
            search(cell)
            getNeighbours(cell)
            drawGrid()
            
pygame.init()
frame = pygame.display.set_mode((screenWidth, screenWidth))
pygame.display.set_caption('Pathfinding Algorithm')
running = True
fillGrid()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while not breadthSearch and not bestSearch:
        drawHomepage()

    drawGrid()
    placeCells()
    deleteCells()

    if bestSearch:
        bestFirstSearch()
    elif breadthSearch:
        breadthFirstSearch()