import pygame

cellWidth = 50
screenWidth = 500
numberOfCells = int(screenWidth / cellWidth)
board = []

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
  

