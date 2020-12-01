import pygame, sys, random
from pygame.locals import *

pygame.init()

size = (600, 480)

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

pygame.display.set_caption('Color-Changer')

fps = pygame.time.Clock()

running = True

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

while running:
    screen.fill(color)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))    

    pygame.display.update()
    fps.tick(120) 
