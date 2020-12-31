import pygame, sys, random, math
from pygame.locals import *

# Using Python 3.9.1 and pygame==2.0.0

pygame.init()

pygame.mouse.set_visible(False)

size = (640, 480)
screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Orbit")

radius = 0 

click = False

fps = pygame.time.Clock()

pos = [0, 0]

col = (0, 0, 0)

circles = []

max_rad = 0
max_pos = 0

done = False

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            click = True

        #else:
        #    click = False

        if event.type == MOUSEBUTTONUP:
            click = False
            done = True

        if event.type == KEYDOWN:
            if event.key == K_r:
                screen.fill((0, 0, 0))
                circles = []
                radius = 0

                pos = [0, 0]

                col = (0, 0, 0)
                
                max_rad = 0
                max_pos = 0

                done = False

            if event.key == K_ESCAPE:
                if not pygame.mouse.set_visible(True):
                    pygame.mouse.set_visible(True)

                else:
                    pygame.mouse.set_visible(False)

            else:
                pygame.mouse.set_visible(False)


    for i in circles:
        pygame.draw.circle(screen, i[0], i[1], i[2])
        
        if i[2] < max_rad: # (x2 - x1), (y2 - y1), atan2(y, x)
            angle = math.atan2(i[1][1] - max_pos[1], i[1][0] - max_pos[0])
            i[1][0] += math.sin(angle)
            i[1][1] -= math.cos(angle)

        if i[1] == max_pos:
            i[1][0] += 0.001
            i[1][1] += 0.001
            
            max_pos = i[1]


    if click:
        radius += 1
        pos = list(pygame.mouse.get_pos())
        col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
        pygame.draw.circle(screen, col, pos, radius)
        #circles.append([col, pos, radius])

        if radius > max_rad:
            max_rad = radius
            max_pos = pos

    if done:
        circles.append([col, pos, radius])
        done = False

    if click != True:
        radius = 0


    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, 10))

    pygame.display.update()
    fps.tick(120)



