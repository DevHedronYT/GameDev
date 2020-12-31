import pygame, random, sys
from pygame.locals import *

# Using Python 3.8.5 and pygame==2.0.0.dev12

def update_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score

def check_collision(rect_1, rect_2):
    if rect_1.colliderect(rect_2):
        return True

    return False

pygame.init()

size = (900, 600)
screen = pygame.display.set_mode(size)


pygame.display.set_caption('Mini-Jam 63')

fps = pygame.time.Clock()

fg = pygame.image.load('files/sprites/fg.png').convert_alpha()
fg = pygame.transform.scale(fg, (900, 50))

fg_x = (0)

bg = pygame.image.load('files/sprites/background.png').convert_alpha()
bg = pygame.transform.scale(bg, size)

player = pygame.image.load('files/sprites/player.png').convert_alpha()
player_rect = player.get_rect(center = (200, 300))
player_speed = 10
pygame.display.set_icon(player)

bullet = pygame.image.load('files/sprites/bullet.png').convert_alpha()
bullet_rect = bullet.get_rect(center = (player_rect.centerx, player_rect.centery))
bullet_speed = 50

asteroid = pygame.image.load('files/sprites/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect(center = (random.randint(0, 800), random.randint(0, 200)))

enemy = pygame.image.load('files/sprites/enemy_space_ship.png').convert_alpha()
enemy_rect = enemy.get_rect(center = (random.randint(0, 800), random.randint(0, 200)))

player_moving_up = False
player_moving_down = False
player_moving_right = False
player_moving_left = False

player_out_of_screen_up = False
player_out_of_screen_down = False
player_out_of_screen_left = False
player_out_of_screen_right = False

asteroid_out_of_screen_left = False

enemy_out_of_screen_x = False
enemy_out_of_screen_y = False

game_font = pygame.font.Font('files/freesansbold.ttf', 32)
white = (241, 240, 238)
red = (151, 63, 63)

score = 0
high_score = 0

shoot = False

running = True

alive = True

menu = True

playing = False

click = False
click2 = False



click_sound = pygame.mixer.Sound('files/music/click.wav')

shoot_sound = pygame.mixer.Sound('files/music/shoot.wav')

explosion = pygame.mixer.Sound('files/music/hit.wav')


while running:


    while menu and playing != True:

        screen.blit(bg, (0,0))

        mx, my = pygame.mouse.get_pos()

        menu_text = game_font.render("Main Menu", False, white)

        play_text = game_font.render("Play Game", False, red)

        screen.blit(menu_text, (size[0] / 2 - 100, size[1] / 2 - 100))

        button = pygame.Rect(350, 300, 200, 50)

        if button.collidepoint((mx, my)):
            if click:
                click_sound.set_volume(0.1)
                click_sound.play()
                menu = False
                playing = True


        pygame.draw.rect(screen, white, button)
        screen.blit(play_text, (360, 300))


        quit_text = game_font.render("Quit Game", False, red)

        button_2 = pygame.Rect(350, 380, 200, 50)

        if button_2.collidepoint((mx, my)):
            if click:
                sys.exit()


        pygame.draw.rect(screen, white, button_2)
        screen.blit(quit_text, (360, 380))

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


    while playing and menu != True:

        screen.blit(bg, (0,0))

        fg_x -= 6
        screen.blit(fg, (fg_x, 580))
        screen.blit(fg, (fg_x + size[0], 580))

        if fg_x <= -900:
            fg_x = 0

        pygame.draw.line(screen, white, [0, 577], [900, 577], 7)

        high_score = update_score(score, high_score)

        asteroid_collision = check_collision(bullet_rect, asteroid_rect)
        player_collision = check_collision(player_rect, asteroid_rect)
        player_collision2 = check_collision(player_rect, enemy_rect)
        enemy_collision = check_collision(bullet_rect, enemy_rect)

        if asteroid_out_of_screen_left:
            asteroid_rect.centerx = 900


        if asteroid_rect.centerx <= 0:
            asteroid_out_of_screen_left = True

        else:
            asteroid_out_of_screen_left = False




        asteroid_rect.centerx -= 7

        if enemy_rect.centery < 0:
            enemy_out_of_screen_y = True

        else:
            enemy_out_of_screen_y = False

        if enemy_rect.centerx < 0:
            enemy_out_of_screen_x = True

        else:
            enemy_out_of_screen_x = False

        if enemy_out_of_screen_y:
            enemy_rect.centery = 600



        if enemy_out_of_screen_x:
            enemy_rect.centerx = 900
            enemy_rect.centery -= 100


        enemy_rect.centerx -= 7




        screen.blit(asteroid, asteroid_rect)
        screen.blit(enemy, enemy_rect)

        if player_collision == False and player_collision2 == False and alive == True:
            screen.blit(player, player_rect)


        if player_collision == True:
            explosion.set_volume(0.5)
            explosion.play()
            alive = False
            score = 0

        if player_collision2 == True:
            explosion.set_volume(0.5)
            explosion.play()
            alive = False
            score = 0

        if alive == False:
            over = game_font.render("Press Space to Play Again", False, white)
            screen.blit(over, (size[0] / 2 - 200, size[1] / 2 - 100))

        score_text = game_font.render("Score: " + str(score), True, white)
        high_score_text = game_font.render("High Score: " + str(high_score), False, white)

        screen.blit(score_text, (707, 50))
        screen.blit(high_score_text, (615, 10))


        if asteroid_collision == True:
            explosion.set_volume(0.5)
            explosion.play()
            screen.blit(asteroid, asteroid_rect)
            asteroid_rect = asteroid.get_rect(center = (random.randint(0, 800), random.randint(0, 200)))
            shoot = False
            score += 1

        if enemy_collision == True:
            explosion.set_volume(0.5)
            explosion.play()
            screen.blit(enemy, enemy_rect)
            enemy_rect = enemy.get_rect(center = (random.randint(0, 800), random.randint(0, 200)))
            shoot = False
            score += 1


        if player_out_of_screen_up:
            player_rect.centery = 580

        if player_out_of_screen_down:
            player_rect.centery = 10

        if player_out_of_screen_left:
            player_rect.centerx = 900

        if player_out_of_screen_right:
            player_rect.centerx = 0

        if player_rect.centerx < 0:
            player_out_of_screen_left = True

        else:
            player_out_of_screen_left = False


        if player_rect.centerx > 900:
            player_out_of_screen_right = True

        else:
            player_out_of_screen_right = False

        if player_rect.centery <= -5:
            player_out_of_screen_up = True

        else:
            player_out_of_screen_up = False

        if player_rect.centery >= 605:
            player_out_of_screen_down = True

        else:
            player_out_of_screen_down = False


        if bullet_rect.centerx > 900:
            bullet_rect = bullet.get_rect(center = (player_rect.centerx, player_rect.centery))
            shoot = False

        if shoot:
            screen.blit(bullet, bullet_rect)
            shoot_sound.set_volume(0.25)
            shoot_sound.play()
            bullet_rect.centerx += bullet_speed

        if player_moving_up:
            player_rect.centery -= player_speed

        if player_moving_down:
            player_rect.centery += player_speed

        if player_moving_left:
            player_rect.centerx -= player_speed

        if player_moving_right:
            player_rect.centerx += player_speed

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w or event.key == K_UP and alive == True:
                    player_moving_up = True

                if event.key == K_s or event.key == K_DOWN and alive == True:
                    player_moving_down = True

                if event.key == K_d or event.key == K_RIGHT and alive == True:
                    player_moving_right = True

                if event.key == K_a or event.key == K_LEFT and alive == True:
                    player_moving_left = True

                if event.key == K_SPACE and alive == True:
                    shoot = True

                if event.key == K_SPACE and alive == False:
                    alive = True
                    player_rect = player.get_rect(center = (200, 300))

                if event.key == K_ESCAPE:
                    menu = True
                    playing = False

            if event.type == KEYUP:
                if event.key == K_w or event.key == K_UP:
                    player_moving_up = False

                if event.key == K_s or event.key == K_DOWN:
                    player_moving_down = False

                if event.key == K_d or event.key == K_RIGHT:
                    player_moving_right = False

                if event.key == K_a or event.key == K_LEFT:
                    player_moving_left = False

        pygame.display.update()
        fps.tick(120)
