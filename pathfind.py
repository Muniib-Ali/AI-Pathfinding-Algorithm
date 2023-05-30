import pygame

cellWidth = 50
screenWidth = 500
numberOfCells = int(screenWidth / cellWidth)
board = []


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

    def makeCanSearch(self):
        self.colour = "yellow"
        
def drawLines():
  
    for i in range(numberOfCells):
        pygame.draw.line(frame, "black", (0, cellWidth * i), (screenWidth, cellWidth * i))

    for i in range(numberOfCells):
        pygame.draw.line(frame, "black", (cellWidth * i,0), (cellWidth * i, screenWidth))
    pygame.display.flip()

pygame.init()

frame = pygame.display.set_mode((screenWidth, screenWidth))
running = True

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    frame.fill("white")
    drawLines()
    pygame.display.flip()
  

