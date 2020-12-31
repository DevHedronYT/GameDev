import pygame, sys, random, time, math
from pygame.locals import *

# Using Python 3.8.6 and pygame==2.0.0.dev16

def sprites(image_path, num_of_images):
    image_list = [pygame.image.load(image_path + str(i) + '.png').convert_alpha() for i in range(num_of_images)]
    return image_list

def flip_sprites(image_list):
    flipped_sprites = [pygame.transform.flip(a, True, False) for a in image_list]
    return flipped_sprites

def gen_chunk(x, y, chunk_size):
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos

            tile_type = 0

            if target_y > 10:
                tile_type = 2

            elif target_y == 10:
                tile_type = 1

            elif target_y == 9:
                if random.randint(1, 5) == 1:
                    tile_type = 3

            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data




def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)

    return collisions

def move_func(rect, movement, tiles):
    collision_types = {'top' : False, "bottom" : False, "right" : False, "left" : False}

    rect.x += movement[0]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True


    rect.y += movement[1]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True

        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


def draw_bg(bg, bg_x, bg_y, screen_width):
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(bg, (bg_x + screen_width, bg_y))

# 640 / 20

pygame.init()
pygame.mixer.init()

size = (640, 480)
screen = pygame.display.set_mode(size, 0, 32)

pygame.mouse.set_visible(False)

display = screen.copy()
display.set_alpha(220)

display.set_colorkey((255,0,0))

pygame.display.set_caption('Noveen')

font = pygame.font.Font('files/text.ttf', 40)
font2 = pygame.font.Font('files/text.ttf', 50)
white = (255, 255, 255)
black = (0, 0, 0)
white_two = (230, 255, 255)

running = True
in_menu = True
playing = False
in_space = True
on_ground = False
make_lvl = False

chunk_size = 8

fps = pygame.time.Clock()

space_bg = pygame.transform.scale(pygame.image.load('files/sprites/worlds/space.png').convert_alpha(), (size[0], size[1]))
space_bg_rect = space_bg.get_rect(center = (0, 0))

spaceship = pygame.transform.scale(pygame.image.load('files/sprites/spaceship.png').convert_alpha(), (175, 175))
menu_spaceship_rect = pygame.Rect(size[0] / 2 - 60, size[1] / 2 + 50, 200, 200)
spaceship_rect = pygame.Rect(-200, size[1] / 2 - 70, 128, 128)

cursor_image = pygame.transform.scale(pygame.image.load('files/sprites/cursor.png').convert_alpha(), (64, 64))
cursor_image.set_colorkey((0, 0, 0))

planet_globe_index = 0

planets = []
planet_globe_rect = pygame.Rect(size[0] / 2 - 65, size[1] / 2 - 50, 64, 64)

for i in range(1, 10):
    planets.append(pygame.transform.scale(pygame.image.load('files/sprites/worlds/planet_' + str(i) + '_globe.png').convert_alpha(), (random.randint(124, 128), 128)))

planet_bgs = []
planet_rect = pygame.Rect(0, 0, size[0], size[1])
for i in range(1, 10):
    planet_bgs.append(pygame.transform.scale(pygame.image.load('files/sprites/worlds/planet_' + str(i) + '.png').convert_alpha(), (size[0], size[1])))


hole_scale = (random.randint(56, 64), random.randint(56, 64))
hole = pygame.transform.scale(pygame.image.load('files/sprites/hole.png').convert_alpha(), hole_scale)
hole_rect = pygame.Rect(size[0] / 2 + random.randint(50, 200), size[1] / 2, 56, 56)

click = False
click_two = False

draw_planet = False

pygame.display.set_icon(space_bg)

gun = pygame.transform.scale(pygame.image.load('files/sprites/weapons/shotgun.png').convert_alpha(), (62, 10))

bg = pygame.transform.scale(pygame.image.load('files/sprites/bg.png'), (size[0], size[1]))
bg_rect = (0, 0)

tile = pygame.transform.scale(pygame.image.load('files/sprites/tile_1.png'), (32, 32))

tile_2 = pygame.transform.scale(pygame.image.load('files/sprites/tile_2.png'), (32, 32))


enemy_follow = pygame.transform.scale(pygame.image.load('files/sprites/enemy/enemy_run/enemy_run_' + str(0) + '.png').convert_alpha(), (64, 64))

enemies = []

for i in range(10, 15):
    enemies.append(pygame.Rect(random.randint(-400, 400), random.randint(-600, 200), 60, 60))

#enemy_death = pygame.transform.scale(pygame.image.load('files/sprites/enemy/enemy_death/enemy_death.png').convert_alpha(), (64, 64))

game_map = {}

tile_index = {
                1: tile,
                2: tile_2,
                3: tile,
                4: enemy_follow
             }



player_idle_frames = []

player_idle_frames.append(pygame.transform.scale(pygame.image.load('files/sprites/player/player_idle/player_idle_' + str(0) + '.png').convert_alpha(), (64, 64)))
player_idle_frames.append(pygame.transform.scale(pygame.image.load('files/sprites/player/player_idle/player_idle_' + str(1) + '.png').convert_alpha(), (64, 64)))

player_idle_frames_index = 0

player_idle_frames_flipped = flip_sprites(player_idle_frames)

player_run_frames = []

for i in range(0, 15):
    player_run_frames.append(pygame.transform.scale(pygame.image.load('files/sprites/player/player_run/player_run_' + str(i) + '.png').convert_alpha(), (64, 64)))

player_run_frame_index = 0

player_run_frames_flipped = flip_sprites(player_run_frames)

player_move = False

player_move_up = False
player_move_down = False
player_move_left = False
player_move_right = False

player_left = False
player_right = False
player_jump = False
player_dash = False

look_left = False
look_right = True

player_speed = 7

vertical_momentum = 0

air_timer = 0
dash_timer = 0
gun_timer = 0

player_rect = pygame.Rect(50, 50, 32, 55)

true_scroll = [0, 0]

framerate = 120

planet_index = random.randint(1, 9)

last_time = time.time()

enemy_exist = True

pygame.mixer.music.load('files/music/music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.075)


direction = None

bx, by = 0, 0
shoot = False
bullet_move = False

gun_rotation = None

jump_sound = pygame.mixer.Sound('files/music/jump.wav')
shoot_sound = pygame.mixer.Sound('files/music/shoot.wav')
destroy_sound = pygame.mixer.Sound('files/music/hurt.wav')
click_sound = pygame.mixer.Sound('files/music/click.wav')

shoot_sound.set_volume(0.5)
jump_sound.set_volume(0.4)
destroy_sound.set_volume(0.4)
click_sound.set_volume(0.07)

enemy_vertical_momentum = 0

destroy_bullet = False

count = 0

enemy_gen = False

go_to_another_planet = False

game_end = False

counting = "0"

while running:

    while in_menu and playing != True:

        button_1 = pygame.Rect(size[0] / 2 - 50, size[1] / 2 - 100, 100, size[1] / 2)
        pygame.draw.rect(screen, white_two, button_1)

        button_2 = pygame.Rect(size[0] / 2 - 50, size[1] / 2 + 100, 100, 50)
        pygame.draw.rect(screen, white_two, button_2)

        mx, my = pygame.mouse.get_pos()

        space_bg_rect.centerx -= 1

        draw_bg(space_bg, space_bg_rect.centerx, 0, size[0])

        if space_bg_rect.centerx <= -size[0]:
            space_bg_rect.centerx = 0

        #screen.blit(space_bg, space_bg_rect)

        if planet_globe_index < 8:
            planet_globe_index += 0.025
            screen.blit(planets[int(planet_globe_index)], planet_globe_rect)

        if planet_globe_index > 8:
            planet_globe_index = 0

        screen.blit(spaceship, menu_spaceship_rect)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        menu_text = font2.render("Noveen", True, white_two)
        play_text = font.render("Play", True, white_two)
        quit_text = font.render("Quit", True, white_two)

        screen.blit(menu_text, (size[0] / 2 - 50, size[1] / 2 - 100))
        screen.blit(play_text, (size[0] / 2 - 25, size[1] / 2))
        screen.blit(quit_text, (size[0] / 2 - 20, size[1] / 2 + 120))

        if button_1.collidepoint((mx, my)):
            if click:
                click_sound.play()
                in_menu = False
                playing = True
                in_space = True
                player_rect_2 = pygame.Rect(spaceship_rect.x + 64, spaceship_rect.y + 64, 64, 64)
                planet_globe_index = 0

        if button_2.collidepoint((mx, my)):
            if click:
                sys.exit()

        screen.blit(cursor_image, pygame.mouse.get_pos())

        pygame.display.update()
        fps.tick(framerate)

    while playing and in_menu != True:
        while in_space and on_ground != True and make_lvl != True:

            space_bg_rect.centerx -= 1

            draw_bg(space_bg, space_bg_rect.centerx, 0, size[0])

            if space_bg_rect.centerx <= -size[0]:
                space_bg_rect.centerx = 0

            screen.blit(spaceship, spaceship_rect)

            spaceship_rect.x += 2

            if spaceship_rect.x > size[0]:
                spaceship_rect.x = -200
                draw_planet = True

            if draw_planet:
                screen.blit(planets[planet_index - 1], planet_globe_rect)

                if planet_globe_rect.colliderect(spaceship_rect):
                    on_ground = True
                    in_space = False
                    player_rect_2 = pygame.Rect(spaceship_rect.x + 64, spaceship_rect.y + 64, 64, 64)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        in_space = False
                        playing = False
                        in_menu = True

            screen.blit(cursor_image, pygame.mouse.get_pos())

            pygame.display.update()
            fps.tick(framerate)

        while on_ground and in_space != True and make_lvl != True:

            screen.blit(planet_bgs[planet_index - 1], planet_rect)

            if player_move_up == False and player_move_down == False and player_move_right == False and player_move_left == False:

                if player_idle_frames_index < 2:
                    player_idle_frames_index += 0.065

                if player_idle_frames_index > 2:
                    player_idle_frames_index = 0

                screen.blit(player_idle_frames[int(player_idle_frames_index)], player_rect_2)

            else:
                if player_move_up:
                    player_rect_2.y -= player_speed

                if player_move_down:
                    player_rect_2.y += player_speed

                if player_move_right:
                    player_rect_2.x += player_speed

                if player_move_left:
                    player_rect_2.x -= player_speed

                if player_run_frame_index < 15:
                    player_run_frame_index += 0.09

                if player_run_frame_index > 15:
                    player_run_frame_index = 0


                screen.blit(player_run_frames[int(player_run_frame_index)], player_rect_2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        on_ground = False
                        playing = False
                        in_menu = True

                    if event.key == K_w or event.key == K_UP:
                        player_move_up = True

                    if event.key == K_s or event.key == K_DOWN:
                        player_move_down = True

                    if event.key == K_d or event.key == K_RIGHT:
                        player_move_right = True

                    if event.key == K_a or event.key == K_LEFT:
                        player_move_left = True

                if event.type == KEYUP:
                    if event.key == K_w or event.key == K_UP:
                        player_move_up = False

                    if event.key == K_s or event.key == K_DOWN:
                        player_move_down = False

                    if event.key == K_d or event.key == K_RIGHT:
                        player_move_right = False

                    if event.key == K_a or event.key == K_LEFT:
                        player_move_left = False

            fps_text = font.render("FPS: " + str(int(fps.get_fps())), True, white)
            screen.blit(fps_text, (50, 50))

            if player_rect_2.x >= 590:
                player_rect_2.x = 590

            if player_rect_2.y >= 420:
                player_rect_2.y = 420

            if player_rect_2.x <= 0:
                player_rect_2.x = 5

            if player_rect_2.y <= 0:
                player_rect_2.y = 5

            screen.blit(hole, hole_rect)

            if hole_rect.colliderect(player_rect_2):
                make_lvl = True
                on_ground = False

            screen.blit(cursor_image, pygame.mouse.get_pos())

            pygame.display.update()
            fps.tick(framerate)

        while in_space != True and on_ground != True and make_lvl:
            mx, my = pygame.mouse.get_pos()

            dt = time.time() - last_time
            dt *= framerate
            last_time = time.time()

            screen.fill(black)

            display.fill(black)

            true_scroll[0] += (player_rect.x - true_scroll[0] - 290) / 20
            true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

            scroll = int(true_scroll[0]), int(true_scroll[1])

            tile_rects = []

            for y in range(3):
                for x in range(4):
                    target_x = x - 1 + int(round(scroll[0] / (chunk_size * 32)))
                    target_y = y - 1 + int(round(scroll[1] / (chunk_size * 32)))
                    target_chunk = str(target_x) + ';' + str(target_y)

                    if target_chunk not in game_map:
                        game_map[target_chunk] = gen_chunk(target_x, target_y, chunk_size)

                    for tile in game_map[target_chunk]:
                        screen.blit(tile_index[tile[1]], (tile[0][0] * 32 - scroll[0], tile[0][1] * 32  - scroll[1]))
                        if tile[1] in [1, 2]:
                            tile_rects.append(pygame.Rect(tile[0][0] * 32, tile[0][1] * 32, 28, 28))


            movement = [0, 0]

            if fps.get_fps() < 75:
                movement[1] += vertical_momentum * dt

            else:
                movement[1] += vertical_momentum

            vertical_momentum += 0.5

            if vertical_momentum > 5:
                vertical_momentum = 5

            if player_right:
                if fps.get_fps() < 75:
                    movement[0] += player_speed * dt

                else:
                    movement[0] += player_speed
                look_right = True
                look_left = False

            if player_left:
                if fps.get_fps() < 75:
                    movement[0] -= player_speed * dt

                else:
                    movement[0] -= player_speed

                look_right = False
                look_left = True

            if player_jump:
                if air_timer < 2:
                    jump_sound.play()

                    if fps.get_fps() < 75:
                        vertical_momentum += 0.1
                        vertical_momentum -= (player_speed - 2)

                    else:
                        vertical_momentum += 0.1
                        vertical_momentum -= player_speed

            if player_dash:
                dash_timer += 1
                if dash_timer < 2:
                    if look_right:
                        if fps.get_fps() < 75:
                            movement[0] += 100 * 2 * dt

                            true_scroll[0] += (player_rect.x - true_scroll[0] - 290) / 20
                            true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

                            scroll = int(true_scroll[0]), int(true_scroll[1])

                        else:
                            movement[0] += 100 * 2

                            true_scroll[0] += (player_rect.x - true_scroll[0] - 290) / 20
                            true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

                            scroll = int(true_scroll[0]), int(true_scroll[1])

                    else:
                        if fps.get_fps() < 75:
                            movement[0] -= 100 * 2 * dt

                            true_scroll[0] += (player_rect.x - true_scroll[0] - 290) / 20
                            true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

                            scroll = int(true_scroll[0]), int(true_scroll[1])

                        else:
                            movement[0] -= 100 * 2

                            true_scroll[0] += (player_rect.x - true_scroll[0] - 290) / 20
                            true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

                            scroll = int(true_scroll[0]), int(true_scroll[1])

            player_rect, collisions = move_func(player_rect, movement, tile_rects)

            if player_dash != True:
                dash_timer = 0

            if collisions['bottom']:
                if enemy_gen != True:
                    enemy_gen = True
                vertical_momentum = 0
                air_timer = 0

            else:
                air_timer += 1

            if player_jump == False and player_right == False and player_left == False:

                if player_idle_frames_index < 2:
                    player_idle_frames_index += 0.045

                if player_idle_frames_index > 2:
                    player_idle_frames_index = 0

                if look_right and look_left != True:
                    screen.blit(player_idle_frames[int(player_idle_frames_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))

                if look_left and look_right != True:
                    screen.blit(player_idle_frames_flipped[int(player_idle_frames_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))


            else:
                if player_jump != True:
                    if player_run_frame_index < 15:
                        player_run_frame_index += 0.2

                    if player_run_frame_index >= 15:
                        player_run_frame_index = 0

                    if look_right and look_left != True:
                        screen.blit(player_run_frames[int(player_run_frame_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))

                    if look_left and look_right != True:
                        screen.blit(player_run_frames_flipped[int(player_run_frame_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))

                else:
                    if look_right and look_left != True:
                        screen.blit(player_idle_frames[int(player_idle_frames_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))

                    if look_left and look_right != True:
                        screen.blit(player_idle_frames_flipped[int(player_idle_frames_index)], (player_rect.x - 16 - scroll[0], player_rect.y - 8 - scroll[1]))


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        shoot_sound.play()
                        shoot = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        make_lvl = False
                        playing = False
                        in_menu = True

                    if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                        player_jump = True

                    if event.key == K_s or event.key == K_DOWN:
                        player_dash = True

                    if event.key == K_d or event.key == K_RIGHT:
                        player_right = True

                    if event.key == K_a or event.key == K_LEFT:
                        player_left = True

                if event.type == KEYUP:
                    if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                        player_jump = False

                    if event.key == K_s or event.key == K_DOWN:
                        player_dash = False

                    if event.key == K_d or event.key == K_RIGHT:
                        player_right = False

                    if event.key == K_a or event.key == K_LEFT:
                        player_left = False

            gun_rect = (player_rect.centerx - 32 - scroll[0], player_rect.centery - scroll[1])
            direction = math.atan2(my - gun_rect[1], mx - gun_rect[0])

            bx += math.cos(direction) * 20
            by += math.sin(direction) * 20

            bullet_rect = pygame.Rect(bx, by, 5, 5)

            if look_right:

                if -math.degrees(direction) < -60:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), (gun_rect[0] + 8, gun_rect[1]))

                elif -math.degrees(direction) > 30:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), (gun_rect[0] + 8, gun_rect[1] - 32))

                else:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), gun_rect)

            else:

                if -math.degrees(direction) < -60:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), (gun_rect[0] + 8, gun_rect[1]))

                elif -math.degrees(direction) > 0:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), (gun_rect[0] + 8, gun_rect[1] - 32))

                else:
                    screen.blit(pygame.transform.rotate(gun, -math.degrees(direction)), gun_rect)

            if shoot != True:
                shoot_timer = 0

            if shoot:
                shoot_timer += 1
                if shoot_timer < 2:
                    bx, by = gun_rect[0], gun_rect[1]

                    bullet_move = True

                    shoot = False

            if destroy_bullet:
                bullet_move = False
                destroy_bullet = False
                bullet_rect = None

            if bullet_move:
                if destroy_bullet != True:

                    pygame.draw.rect(screen, (255, 255, 255), bullet_rect)

            display_r = pygame.Rect(scroll[0], scroll[1], size[0], size[1])

            if enemy_gen:
                    for enemy in enemies:
                        if display_r.colliderect(enemy):
                            enemy_vertical_momentum += 0.5

                            if enemy_vertical_momentum > 5:
                                enemy_vertical_momentum = 5

                            enemy_movement = [0, vertical_momentum]

                            if player_rect.x > enemy.x + random.randint(5, 10): #enemy[1].x
                                enemy_movement[0] = random.randint(2, 4)

                            if player_rect.x < enemy.x - random.randint(5, 10):
                                enemy_movement[0] = -random.randint(2, 4)

                            if player_rect.y > enemy.y + random.randint(5, 10):
                                enemy_movement[1] = random.randint(1, 3)

                            if player_rect.y < enemy.y - random.randint(5, 10):
                                enemy_movement[1] = -random.randint(1, 3)

                            index = enemies.index(enemy)


                            enemy_rect, collision_types = move_func(enemy, enemy_movement, tile_rects)

                            enemy = pygame.Rect(enemy_rect.x - scroll[0], enemy_rect.y - scroll[1], 60, 60)

                            if collision_types['bottom'] == True:
                                enemy_vertical_momentum = 0

                            if player_rect.colliderect(enemy_rect):
                                player_rect = pygame.Rect(50, 50, 32, 55)
                                count = int(counting)
                                enemy_gen = False

                            if enemy.collidepoint((bx, by)):
                                destroy_bullet = True
                                enemies.pop(index)
                                enemies.append(pygame.Rect(random.randint(0, 400), random.randint(0, 200), 60, 60))
                                destroy_sound.play()
                                count += 1

                            display.blit(enemy_follow, enemy)

            if count > 25:
                gun = pygame.transform.scale(pygame.image.load('files/sprites/weapons/spit.png').convert_alpha(), (62, 10))
                counting = "25"

            if count > 75:
                gun = pygame.transform.scale(pygame.image.load('files/sprites/weapons/pistol.png').convert_alpha(), (62, 10))
                counting = "75"

            if count > 150:
                gun = pygame.transform.scale(pygame.image.load('files/sprites/weapons/rifle.png').convert_alpha(), (62, 10))
                counting = "150"

            if count > 250:
                in_space = False
                on_ground = False
                make_lvl = False
                game_end = True

            fps_text = font.render("FPS: " + str(int(fps.get_fps())), True, white)
            display.blit(fps_text, (50, 10))

            enemies_killed = font.render("Enemies Busted: " + str(int(count)), True, white)
            display.blit(enemies_killed, (50, 35))

            pygame.draw.circle(display, (255, 0, 0), (player_rect.centerx - scroll[0], player_rect.centery - scroll[1]), 64)

            display.blit(cursor_image, pygame.mouse.get_pos())

            screen.blit(pygame.transform.scale(display, (size[0], size[1])), (0, 0))

            pygame.display.update()
            fps.tick(framerate)

        while in_space != True and on_ground != True and make_lvl != True and game_end:
            screen.fill((black))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    pygame.quit()
                    sys.exit()


            finale = font.render("Congrats You Have Finished The Game", True, white)
            screen.blit(finale, (size[0] / 2 - 250, size[1] / 2 - 100))

            quit = font.render("Press Any Key to Quit", True, white)
            screen.blit(quit, (size[0] / 2 - 150, size[1] / 2))

            pygame.display.update()
            fps.tick(framerate)
