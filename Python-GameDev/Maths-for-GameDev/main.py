import pygame, sys, math
from pygame.locals import * 

# Using Python 3.9.1 and pygame==2.0.0

pygame.init()
pygame.font.init()

fonts = {}
def text(text, color, size, x, y, font):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font, size)
    screen.blit(fonts[size].render(text, False, color), (x, y))

pygame.mouse.set_visible(False)

size = (1400, 900)

screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Maths for Game Dev")

fps = pygame.time.Clock()
font = "m6x11.ttf"

r = 0 
g = 0
b = 0
increase = 0.75

add = True

pen_colors = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_count = 0

press = 0

press_three_mcoords = []

triangle = True
three_draw = False
three_rects = []

three_erase = False

press_four_mcoords = []

vector = True
four_draw = False
four_rects = []

four_erase = False

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
            if event.key == K_RIGHT or event.key == K_SPACE:
                press += 1

            if event.key == K_LEFT:
                press -= 1

            if event.key == K_u and press == 3:
                three_erase = True

            if event.key == K_u and press == 4:
                four_erase = True

            if event.key == K_d and press == 3 and triangle == True and len(press_three_mcoords) > 2:
                triangle = False

            if event.key == K_d and press == 4 and vector == True and len(press_four_mcoords) > 2:
                vector = False

            if event.key == K_e and press == 3:
                three_rects.clear()
                press_three_mcoords.clear()

            if event.key == K_e and press == 4:
                four_rects.clear()
                press_four_mcoords.clear()

            if event.key == K_c:
                color_count += 1

            if event.key == K_p and press == 3:
                triangle = True

            if event.key == K_p and press == 4:
                vector = True

        if event.type == KEYUP:
            if event.key == K_u and press == 3:
                three_erase = False

            if event.key == K_u and press == 4:
                four_erase = False

        if event.type == MOUSEBUTTONDOWN:

            if event.button == 1 and press == 3:
                if triangle == False:
                    three_draw = True

                if triangle:
                    press_three_mcoords.append(pygame.mouse.get_pos())     
                    if len(press_three_mcoords) > 1:
                        pygame.draw.lines(screen, pen_colors[color_count], False, press_three_mcoords)

            if event.button == 1 and press == 4:
                if vector == False:
                    four_draw = True

                if vector:
                    press_four_mcoords.append(pygame.mouse.get_pos())     
                    if len(press_four_mcoords) > 1:
                        pygame.draw.lines(screen, pen_colors[color_count], False, press_four_mcoords)



        if event.type == MOUSEBUTTONUP:
            if press == 3:
                three_draw = False

            if press == 4:
                four_draw = False
                        
           #     if triangle == False:
           #         three_draw = True
           #         three_rects.append(pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (10, 10)))
           #         for rect in three_rects:
           #             pygame.three_draw.rect(screen, (255, 255, 255), rect)

    if color_count > 4: 
        color_count = 0

    if three_draw:
        three_rects.append(pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (10, 5)))
        for rect in three_rects:
            pygame.draw.rect(screen, pen_colors[color_count], rect)

    if three_erase:
        if triangle:
            if len(press_three_mcoords) > 0:
                press_three_mcoords.pop()

        if triangle == False:
            if len(three_rects) > 0:
                three_rects.pop()


    if four_draw:
        four_rects.append(pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (10, 5)))
        for rect in four_rects:
            pygame.draw.rect(screen, pen_colors[color_count], rect)

    if four_erase:
        if vector:
            if len(press_four_mcoords) > 0:
                press_four_mcoords.pop()

        if vector == False:
            if len(four_rects) > 0:
                four_rects.pop()


    if press == 0:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)
        
        text("Hello, World!", (r, g, b), 40, pygame.display.get_surface().get_size()[0] / 2 - 90, pygame.display.get_surface().get_size()[1] / 2 - 50, font)
        text("Maths for Game Dev", (r, g, b), 20, pygame.display.get_surface().get_size()[0] / 2 - 80, pygame.display.get_surface().get_size()[1] / 2, font)

        text("Slide: " + str(press), (r, g, b), 20, 30, pygame.display.get_surface().get_size()[1] - 100, font)
        text("FPS: " + str(int(fps.get_fps())), (r, g, b), 20, 30, 30, font)

    if press == 1 and press > 0:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)
        
        text("Prerequisites:", (r, g, b), 70, pygame.display.get_surface().get_size()[0] / 2 - 180, 50, font)
        text("Basics of Geometry", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 112, pygame.display.get_surface().get_size()[1] / 2 - 50, font)
        text("Coordinate Geometry", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 120, pygame.display.get_surface().get_size()[1] / 2 - 25, font)    
        text("Algebra", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 60, pygame.display.get_surface().get_size()[1] / 2, font)
        text("Angles", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 60, pygame.display.get_surface().get_size()[1] / 2 + 25, font)        

        text("Slide: " + str(press), (r, g, b), 20, 30, pygame.display.get_surface().get_size()[1] - 100, font)
        text("FPS: " + str(int(fps.get_fps())), (r, g, b), 20, 30, 30, font)

    if press == 2 and press > 0:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)
        
        text("Contents:", (r, g, b), 70, pygame.display.get_surface().get_size()[0] / 2 - 120, 50, font)
        text("Review", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 50, pygame.display.get_surface().get_size()[1] / 2 - 50, font)
        text("Trigonometry", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 85, pygame.display.get_surface().get_size()[1] / 2 - 25, font)
        text("Linear Algebra", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 85, pygame.display.get_surface().get_size()[1] / 2, font)

        text("Slide: " + str(press), (r, g, b), 20, 30, pygame.display.get_surface().get_size()[1] - 100, font)
        text("FPS: " + str(int(fps.get_fps())), (r, g, b), 20, 30, 30, font)

    if press == 3 and press > 0:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)

        if len(press_three_mcoords) > 1 and triangle == True:
            #pygame.three_draw.polygon(screen, (255, 255, 255), press_three_mcoords)
            pygame.draw.lines(screen, pen_colors[color_count], False, press_three_mcoords)
            
        if triangle:
            for rect in three_rects:
                pygame.draw.rect(screen, pen_colors[color_count], rect)

        if triangle == False:
            if len(press_three_mcoords) > 2:
                pygame.draw.polygon(screen, pen_colors[color_count], press_three_mcoords) 
            
            
            if len(three_rects) > 0:
                for rect in three_rects:
                    pygame.draw.rect(screen, pen_colors[color_count], rect)

        text("Slide: " + str(press), (r, g, b), 20, 30, pygame.display.get_surface().get_size()[1] - 100, font)
        text("FPS: " + str(int(fps.get_fps())), (r, g, b), 20, 30, 30, font)

    if press == 4 and press > 0:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)

        if len(press_four_mcoords) > 1 and vector == True:
            #pygame.three_draw.polygon(screen, (255, 255, 255), press_three_mcoords)
            pygame.draw.lines(screen, pen_colors[color_count], False, press_four_mcoords)
            
        if vector:
            for rect in four_rects:
                pygame.draw.rect(screen, pen_colors[color_count], rect)

        if vector == False:
            if len(press_four_mcoords) > 2:
                pygame.draw.polygon(screen, pen_colors[color_count], press_four_mcoords) 
            
            
            if len(four_rects) > 0:
                for rect in four_rects:
                    pygame.draw.rect(screen, pen_colors[color_count], rect)


        text("Slide: " + str(press), (r, g, b), 20, 30, pygame.display.get_surface().get_size()[1] - 100, font)
        text("FPS: " + str(int(fps.get_fps())), (r, g, b), 20, 30, 30, font)


    pygame.display.update()
    fps.tick(120)

