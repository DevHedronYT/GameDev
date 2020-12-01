import pygame, sys, random, math
from pygame.locals import *

pygame.init()

size = (960, 720)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Test')

white = (255, 255, 255)

tile = pygame.image.load('tile_thin.png').convert_alpha()


running = True
playing = True

fps = pygame.time.Clock()

click = False

tile_rects = []

while running:
    while playing:
        screen.fill(white)

        mx, my = pygame.mouse.get_pos()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        if click:
            n = pygame.Rect((mx - 32, my - 32), (32, 32))
            tile_rects.append(n)

        for i in tile_rects:
            screen.blit(tile, i)
            
        if not click:
            n = pygame.Rect((mx - 32, my - 32), (32, 32))
            screen.blit(tile, n)


        pygame.display.update()
        fps.tick(120)
