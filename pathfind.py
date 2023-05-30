import pygame

cellWidth = 10
screenWidth = 1000


pygame.init()

frame = pygame.display.set_mode((screenWidth, screenWidth))
running = True

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    frame.fill("white")
    pygame.display.flip()
  

