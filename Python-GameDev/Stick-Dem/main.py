import pygame, sys, random
from pygame.locals import *

# Using Python 3.8.5 and pygame==2.0.0.dev12

def update_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score

pygame.init()

size = (1400, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('LD-47')

fps = pygame.time.Clock()

game_font = pygame.font.Font('files/text.ttf', 40)
game_font2 = pygame.font.Font('files/text.ttf', 52)
white = (255, 255, 255)
blue = (2, 119, 189)
black = (0, 0, 0)
menu_color = (78, 52, 46)

in_menu = True
playing = False

click = False
click_game = False

collect_sound = pygame.mixer.Sound('files/beep.wav')

loop = pygame.image.load('files/sprites/loop.png').convert_alpha()
loop_rect = loop.get_rect(center = (700, 300))

icon = pygame.display.set_icon(loop)

enemy = pygame.image.load('files/sprites/enemy.png').convert_alpha()
enemy = pygame.transform.scale(enemy, (100, 100))

enemies = []
for i in range(0, 5):
    enemies.append(enemy.get_rect(center = (random.randint(100, 1400), random.randint(100, 800))))

score = 0
high_score = 0

running = True

time = 60000

time_is_up = False

count = 0

timer_enemy = 100000

while running:
    while in_menu and playing != True:

        screen.fill(menu_color)

        mx, my = pygame.mouse.get_pos()

        menu_text = game_font.render("Main Menu", True, white)
        play_text = game_font.render("Play Game", True, black)
        quit_text = game_font.render("Quit Game", True, black)

        button_1 = pygame.Rect(size[0] / 2 - 75, size[1] / 2 - 50, 200, 50)
        button_2 = pygame.Rect(size[0] / 2 - 75, size[1] / 2 + 50, 200, 50)

        pygame.draw.rect(screen, white, button_1)
        pygame.draw.rect(screen, white, button_2)


        screen.blit(menu_text, (size[0] / 2 - 40, size[1] / 2 - 150))
        screen.blit(play_text, (size[0] / 2 - 40, size[1] / 2 - 50))
        screen.blit(quit_text, (size[0] / 2 - 40, size[1] / 2 + 50))

        if button_1.collidepoint((mx, my)):
            if click:
                collect_sound.set_volume(0.75)
                collect_sound.play()
                in_menu = False
                playing = True
                screen.fill(blue)

        if button_2.collidepoint((mx, my)):
            if click:
                sys.exit()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        fps.tick(120)

    while playing and in_menu != True:
        loop_rect = loop.get_rect(center = (700, 300))

        screen.fill(blue)

        if time_is_up == False:
            center = 0

            time -= 10
            mx, my = pygame.mouse.get_pos()


            for i in enemies:
                if i.collidepoint((mx, my)):
                    if click_game:
                        screen.fill(blue)
                        collect_sound.set_volume(0.75)
                        collect_sound.play()
                        score += 1

                        index = enemies.index(i)
                        enemies[index] = enemy.get_rect(center = (random.randint(100, 1400), random.randint(100, 800)))


                elif click_game == False:
                    timer_enemy -= 25

                    if timer_enemy == 0:
                        index = enemies.index(i)
                        enemies[index] = enemy.get_rect(center = (random.randint(100, 1400), random.randint(100, 800)))
                        timer_enemy = 100000

            click_game = False

            screen.blit(loop, loop_rect)

            time_text = game_font2.render("Time Left: " + str(time), True, white)
            screen.blit(time_text, (510, 100))

            fps_text = fps.get_fps()
            fps_text = game_font.render("FPS: " + str(int(fps_text)), True, white)
            screen.blit(fps_text, (10, 10))

            score_text = game_font.render("Entities Stuck in Loop: " + str(score), True, black)
            screen.blit(score_text, (483, 550))

            high_score_text = game_font.render("Highest Entities Stuck: " + str(high_score), True, black)
            screen.blit(high_score_text, (495, 580))

            for i in enemies:
                screen.blit(enemy, i)

            if time == 0:
                time_is_up = True
                time = 60000

        if time_is_up:
            screen.fill(black)

            text = game_font.render("Your score was: " + str(score), True, white)
            screen.blit(text, (540, 400))

            text = game_font.render("Press any key to continue", True, white)
            screen.blit(text, (500, 450))


        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if time_is_up == False:
                    if event.key == K_ESCAPE:
                        in_menu = True
                        playing = False

                else:
                    high_score = update_score(score, high_score)
                    score = 0
                    time_is_up = False

            if time_is_up == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_game = True



        pygame.display.update()
        fps.tick(120)
