import pygame, sys, random
from pygame.locals import *


pygame.init()

size = (640, 480)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Menu Tutorial")

click = False

fps = pygame.time.Clock()

menu_button = pygame.Rect(size[0] / 2 - 50, size[1] / 2, 100, 40)

menu_button_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

menu_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

while True:
    screen.fill(menu_color)

    mx, my = pygame.mouse.get_pos()

    pygame.draw.rect(screen, menu_button_color, menu_button)

    if click:
        if menu_button.collidepoint((mx, my)):
            menu_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            menu_button.x += 20

            menu_button_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    click = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

            sys.exit()

        if event.type == KEYDOWN:
            if event.button == 1:
                click = True

    pygame.display.update()
    fps.tick(120)
