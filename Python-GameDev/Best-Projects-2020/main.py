import pygame, sys
from pygame.locals import * 

pygame.init()
pygame.font.init()

fonts = {}
def text(text, color, size, x, y, font):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font, size)
    screen.blit(fonts[size].render(text, False, color), (x, y))

pygame.mouse.set_visible(False)

size = (960, 720)

screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Pygame Projects 2020")

fps = pygame.time.Clock()
font = "m6x11.ttf"

r = 0 
g = 0
b = 0

increase = 0.75

add = True


while True:

    r += increase
    g += increase
    b += increase


    if add: 
        increase = 0.75

    else:
        increase = 0

    if r >= 255:
        r = 255
        add = False

    if r <= 0:
        add = True

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            pass
        
        if event.type == KEYUP:
            pass

        if event.type == MOUSEBUTTONUP:
            pass
        
           #     if triangle == False:
           #         three_draw = True
           #         three_rects.append(pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (10, 10)))
           #         for rect in three_rects:
           #             pygame.three_draw.rect(screen, (255, 255, 255), rect)


    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)
        
    text("Happy New Year! Today I am going to showing off some of my best projects that I made in the past year...", (r, g, b), 20, 23, 50, font)
    text("It was quite a tough year but I made some interesting projects along the way", (r, g, b), 20, 23, 80, font)
    text("For some I followed a lot of tutorials, while others I made just for fun or experience", (r, g, b), 20, 23, 110, font)

    text("1. Orbit Simulator (Simulation of Planets Orbiting Each Other?)", (r, g, b), 20, 70, 160, font)
    text("2. Isometric Productivity (Simple Isometric Game)", (r, g, b), 20, 70, 190, font)
    text("3. Noveen (Made for 5 Game Jams)", (r, g, b), 20, 70, 220, font)
    text("4. Platformer (Followed DaFluffyPotato's Tutorials)", (r, g, b), 20, 70, 250, font)
    text("5. Maths for Game Dev Program (Made for Maths for Game Dev Video)", (r, g, b), 20, 70, 280, font)
    text("6. Escape the Island (Made for Pyweek-30)", (r, g, b), 20, 70, 310, font)
    text("7. Stick-Dem (Made for Ludum Dare 47)", (r, g, b), 20, 70, 340, font)

    text("Everything should be on GitHub except for Number 4, since that is not really my original code :)", (r, g, b), 20, 23, 390, font)
    text("The Program I wrote for this Video will also be on GitHub", (r, g, b), 20, 23, 420, font)

    text("Credits to Daniel Linsson for the Font", (r, g, b), 40, pygame.display.get_surface().get_size()[0] / 2 - 350, 500, font)

 
#    text("It was quite a tough year but I made some interesting projects along the way: ", (r, g, b), 20, 30, 80, font)
#    text("It was quite a tough year but I made some interesting projects along the way: ", (r, g, b), 20, 30, 80, font)
#    text("It was quite a tough year but I made some interesting projects along the way: ", (r, g, b), 20, 30, 80, font)
#    text("It was quite a tough year but I made some interesting projects along the way: ", (r, g, b), 20, 30, 80, font)


    pygame.display.update()
    fps.tick(140)

