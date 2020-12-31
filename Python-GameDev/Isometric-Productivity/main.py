import pygame, sys, random, math
from pygame.locals import *

# Using Python 3.9 and pygame==2.0.0

#pygame.mixer.pre_init(frequency=22050)
pygame.init()

def draw_bg(bg, bg_x, bg_y, screen_height, screen):
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(bg, (bg_x, bg_y + screen_height))

def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    product = []
    for line in data:
        product.append(list(line))
    return product

a = 1
a2 = 26.6

matrix = [
    [a, round(-math.tan(math.radians(a2)), 3)],
    [a, round(math.tan(math.radians(a2)), 3)]
]

def transform_cords(cords):
    cords = [cords[1] * 32, cords[0] * 32]
    return [(cords[0] * matrix[0][0]) + (cords[1] * matrix[1][0]),
            (cords[0] * matrix[0][1]) + (cords[1] * matrix[1][1])]

def blit_map(map, offset):
    #y = offset[1] + len(map[0])-1
    y = offset[1] 
    x = offset[0] 

    tile_rects = []

    for ind in range(0, len(map)):
        for block in map[ind]:
            if block == "1":
                iso = transform_cords([x, y])
                rect = pygame.Rect(tuple(iso), (32, 32))
                tile_rects.append(rect)

            x += 1
        y -= 1
        x = offset[0]

    return tile_rects



size = (960, 720)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Productivity')

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("files/text.ttf", 50)
font2 = pygame.font.Font("files/text.ttf", 40)

map = load_map("files/map.txt")

tile = pygame.image.load('files/sprites/tile_thin.png').convert_alpha()
tile_down = pygame.image.load('files/sprites/tile.png').convert_alpha()
plant_tile = pygame.image.load('files/sprites/plant.png').convert_alpha()


running = True
playing = True

fps = pygame.time.Clock()

click = False

#tile_rects = blit_map(map, [17, -5])

#tile_rects2 = blit_map(map, [17, -5])

tile_rects = blit_map(map, [17, -2])

tile_rects2 = blit_map(map, [17, -2])

tile_rects3 = []

bg = pygame.transform.scale(pygame.image.load('files/sprites/bg3.png').convert_alpha(), (size[0], size[1]))
bg_rect = bg.get_rect(center = (0, 0))

index = None

click_right = False

num_of_seeds = 0

max_time = None

start_time = False

seconds = None

num = None

time = 0

time_up = False

score = 0

planting = pygame.mixer.Sound('files/sounds/plant.wav')
planting.set_volume(0.5)

deplant = pygame.mixer.Sound('files/sounds/plant2.wav')
deplant.set_volume(0.5)

while running:

    while playing and time_up == False:

        screen.fill(white)
        bg_rect.centery -= 1

        draw_bg(bg, bg_rect.centerx, bg_rect.centery, size[1], screen)

        if bg_rect.centery <= -size[1]:
            bg_rect.centery = 0

        mx, my = pygame.mouse.get_pos()

        click = False
        click_right = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        for i in tile_rects2:
            screen.blit(tile_down, (i.x - 16, i.y - 8))

        for i in tile_rects:
            screen.blit(tile, (i.x - 16, i.y - 8))

            if i.collidepoint((mx, my)) and click:
                planting.play()
                
                index = tile_rects.index(i)

                tile_rects3.append(tile_rects[index])

                tile_rects.pop(index)

                click = False
                
                num_of_seeds += 1

                start_time = True
            
        for i in tile_rects3:
            screen.blit(plant_tile, (i.x - 16, i.y - 8))

            if i.collidepoint((mx, my)) and click:
                deplant.play()

                index = tile_rects3.index(i)

                tile_rects.append(tile_rects3[index])

                tile_rects3.pop(index)

                click = False
                          
                num_of_seeds -= 1


        if start_time:
            time += 1

            prod_text = font2.render("Do Something Productive for 25 minutes / 1500 Seconds", True, white)
            screen.blit(prod_text, (size[0] / 2 - 375, size[1] / 2 - 300))

            time_text = font2.render("Seconds Passed: " + str(int(time / 120)), True, white)
            screen.blit(time_text, (size[0] / 2 - 100, size[1] / 2 - 270))

        if int(time / 120) >= 1500:
            time = 0
            start_time = False
            time_up = True
            playing = False
            tile_rects = blit_map(map, [17, -5])
            tile_rects2 = blit_map(map, [17, -5])
            tile_rects3 = []

        score_text = font2.render('Score: ' + str(score), True, white)
        screen.blit(score_text, (size[0] / 2 + 200, size[1] / 2 + 200))


        pygame.display.update()
        fps.tick(120)

    while time_up:
        text = font.render("Press anything to reset and start the timer again", True, white)
        screen.blit(text, (size[0] / 2 - 425, size[1] / 2))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                playing = True
                time_up = False
                score += 10


        pygame.display.update()
        fps.tick(120)
