import pygame, random, sys, math
from pygame.locals import *

# Using Python 3.9.1 and pygame==2.0.1

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read().split("\n")
    f.close()
    
    game_map = []

    for row in data:
        game_map.append(list(row))

    return game_map

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font, size)
    surface.blit(fonts[size].render(text, False, color), (x, y))

def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list

def move(rect, movement, tiles):
    collision_types = {
                            "top"    : False,
                            "bottom" : False,
                            "right"  : False,
                            "left"   : False

                      }

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True

        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True

    return rect, collision_types


global animation_frames
animation_frames = {}

def load_animation(path, frame_durations, animation_name):
    global animation_frames

    animation_frame_data = []

    n = 0

    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_image.set_colorkey((33, 150, 243))
        animation_frames[animation_frame_id] = animation_image.copy()
    
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)

        n += 1 

    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0

    return action_var, frame

def centered_rotation(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

size = (960, 720)

screen = pygame.display.set_mode(size, RESIZABLE)
display = pygame.Surface((480, 360))
#display = pygame.Surface((720, 540))

pygame.display.set_caption("Gain")

fps = pygame.time.Clock()

font = "files/font/m6x11.ttf"

upper_tile = pygame.image.load('files/sprites/tiles/tile_0.png').convert_alpha()
lower_tile = pygame.image.load('files/sprites/tiles/tile_1.png').convert_alpha()

pygame.display.set_icon(upper_tile)

tile_size = (upper_tile.get_width(), upper_tile.get_height())

game_map = load_map("map")

animation_database = {}

animation_database["idle"] = load_animation("files/sprites/player/idle/with_weapon", [10, 10, 20], "idle")
animation_database["run"] = load_animation("files/sprites/player/run/with_weapon", [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "run")
animation_database["jump"] = load_animation("files/sprites/player/jump", [5000, 5000], "jump")
animation_database["block"] = load_animation("files/sprites/player/attack/block", [5000, 5000], "block")

gun = pygame.image.load("files/sprites/player/attack/shotgun.png").convert_alpha()

player_action = "idle"
player_frame = 0
player_flip = False

moving_right = False
moving_left = False

shoot = False
bullet_move = False
bx, by = 0, 0
direction = None

player_y_momentum = 0

player_rect = pygame.Rect(600, 800, 18, 27)

air_timer = 0
shoot_timer = 0

shoot_ = 0

destroy_bullet = False

subs = 0
sub_goal = 2000000

true_scroll = [0, 0]

block = False

click = False

in_menu = False
in_cutscene = True
playing = False

coin = pygame.image.load("files/sprites/coin/coin.png").convert_alpha()

coin_pos = []
for i in range(5):
    coin_pos.append(pygame.Rect(random.randint(0, 960), random.randint(0, 480), 32, 32))

enemy_image = pygame.image.load("files/sprites/enemy/enemy.png").convert_alpha()

enemy_y_momentum = 0
enemies = []

for i in range(10, 15):
    enemies.append(pygame.Rect(random.randint(0, 960), random.randint(0, 480), 32, 32))

r = 0 
g = 0
b = 0
increase = 0.75
add = True

timer = 0

particles = []

screen_shake = 0

shake_timer = 0

pygame.mixer.music.load('files/music/music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.075)

jump_sound = pygame.mixer.Sound('files/music/jump.wav')
shoot_sound = pygame.mixer.Sound('files/music/shoot.wav')
destroy_sound = pygame.mixer.Sound('files/music/hurt.wav')
click_sound = pygame.mixer.Sound('files/music/click.wav')

shoot_sound.set_volume(0.5)
jump_sound.set_volume(0.4)
destroy_sound.set_volume(0.4)
click_sound.set_volume(0.07)


while True:

    while in_cutscene and not playing and not in_menu:
        screen.fill((0, 0, 0))

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
        
        if timer < 600:
            text("Once Upon a Terrible Time...", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 140, pygame.display.get_surface().get_size()[1] / 2 - 50, font, screen)
            text("There was a guy named Dani", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 140, pygame.display.get_surface().get_size()[1] / 2, font, screen)

            if timer < 500 and timer > 200:
                r -= increase
                g -= increase
                b -= increase

        if timer > 600 and timer < 700:
            r = 0
            g = 0
            b = 0

        if timer < 1200 and timer > 650:
            text("He needed help...", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 170, pygame.display.get_surface().get_size()[1] / 2 - 50, font, screen)
            text("In Getting 2 Million Subs", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 170, pygame.display.get_surface().get_size()[1] / 2, font, screen)
            text("Now go help him!", (r, g, b), 30, pygame.display.get_surface().get_size()[0] / 2 - 170, pygame.display.get_surface().get_size()[1] / 2 + 50, font, screen)

        if timer > 1200:
            in_menu = True
            in_cutscene = False


        timer += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                timer += 200


        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)

        pygame.display.update()
        fps.tick(120) 

    while in_menu and not in_cutscene and not playing:

        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(pygame.display.get_surface().get_size()[0] / 2 - 150, pygame.display.get_surface().get_size()[1] / 2 - 60, 300, 50)
        quit_button = pygame.Rect(pygame.display.get_surface().get_size()[0] / 2 - 150, pygame.display.get_surface().get_size()[1] / 2 + 30, 300, 50)

        pygame.draw.rect(screen, (0, 0, 0), play_button)
        pygame.draw.rect(screen, (0, 0, 0), quit_button)

        text("Gain", (255, 255, 255), 60, pygame.display.get_surface().get_size()[0] / 2 - 50, pygame.display.get_surface().get_size()[1] / 2 - 200, font, screen)
        text("Play", (255, 255, 255), 30, pygame.display.get_surface().get_size()[0] / 2 - 30, pygame.display.get_surface().get_size()[1] / 2 - 60, font, screen)
        text("Quit", (255, 255, 255), 30, pygame.display.get_surface().get_size()[0] / 2 - 30, pygame.display.get_surface().get_size()[1] / 2 + 30, font, screen)

        if play_button.collidepoint((mx, my)):
            if click:
                click_sound.play()
                playing = True
                in_menu = False

        if quit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 4)

        pygame.display.update()
        fps.tick(120)


    while playing and not in_cutscene and not in_menu:
        screen.fill((0, 0, 0))
        display.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        #true_scroll[0] += (player_rect.x - true_scroll[0] - 395) / 20
        true_scroll[0] += (player_rect.x - true_scroll[0] - 260) / 10

        #true_scroll[1] += (player_rect.y - true_scroll[1] - 300) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 10


        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        if screen_shake and shake_timer < 10000:
            scroll[0] += random.randint(0, 8) - 4
            scroll[1] += random.randint(0, 8) - 4
            shake_timer += 100

        if shake_timer > 10000:
            screen_shake = 0
            shake_timer = 0

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(lower_tile, (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                if tile == '2':
                    display.blit(upper_tile, (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))

                x += 1
                
            y += 1

        player_movement = [0, 0]

        gun_rect = pygame.Rect(player_rect.centerx - 16 - scroll[0], player_rect.centery - scroll[1], 26, 4)
        # direction = math.atan2(my - gun_rect.y, mx - gun_rect.x)
        direction = math.atan2((pygame.mouse.get_pos()[1] / (pygame.display.get_surface().get_size()[1] / 360)) - gun_rect.y, (pygame.mouse.get_pos()[0] / (pygame.display.get_surface().get_size()[0] / 480)) - gun_rect.x)

        bx += math.cos(direction) * 20
        by += math.sin(direction) * 20

        bullet_rect = pygame.Rect(bx, by, 5, 5)

        if shoot:
            if shoot_timer < 1.2:
                bx, by = gun_rect[0], gun_rect[1]
                
                player_movement[0] -= math.cos(direction) * 30
                player_movement[1] -= math.sin(direction) * 30

                bullet_move = True

                shoot_ += 1

                shoot = False


        if bullet_move:
            if bullet_rect.x > 960 or bullet_rect.x < -960:
                screen_shake = 0
                bullet_move = False
                destroy_bullet = False
                
            else:
                pygame.draw.rect(display, (255, 255, 255), bullet_rect)


        if moving_right:
            player_movement[0] += 5

        if moving_left:
            player_movement[0] -= 5

        player_movement[1] += player_y_momentum
        player_y_momentum += 0.5

        if player_y_momentum >= 5:
            player_y_momentum = 5
        
        if enemy_y_momentum >= 3:
            enemy_y_momentum = 3

        if player_movement[0] > 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "run")
            player_flip = False

        if player_movement[0] < 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "run")
            player_flip = True

        if player_movement[0] == 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "idle")

        if player_movement[1] < 0:
            player_action, player_frame = change_action(player_action, player_frame, "jump")

        if air_timer > 20:
            player_action, player_frame = change_action(player_action, player_frame, "jump")
        
        if block and air_timer == 0 and player_movement[0] == 0:
            player_action, player_frame = change_action(player_action, player_frame, "block")
            player_movement = [0, 0]

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions["bottom"]:
            player_y_momentum = 0
            air_timer = 0

        else:
            air_timer += 0.5

        if air_timer > 320:
            player_rect.x, player_rect.y = 600, 800
            air_timer = 0

        if collisions["top"]:
            player_y_momentum += 2

        display_r = pygame.Rect(scroll[0], scroll[1], pygame.display.get_surface().get_size()[0], pygame.display.get_surface().get_size()[1])
        
        #if player_y_momentum == 0:
        for enemy in enemies:
            if display_r.colliderect(enemy):
                enemy_y_momentum += 1

                if enemy_y_momentum > 3:
                    enemy_y_movement = 3

                enemy_movement = [0, player_y_momentum - 5]

                if player_rect.x > enemy.x + random.randint(5, 10): #enemy[1].x
                    enemy_movement[0] = random.randint(1, 2)

                if player_rect.x < enemy.x - random.randint(5, 10):
                    enemy_movement[0] = -random.randint(1, 2)

                if player_rect.y > enemy.y + random.randint(5, 10):
                    enemy_movement[1] = random.randint(1, 2)

                if player_rect.y < enemy.y - random.randint(5, 10):
                    enemy_movement[1] = -random.randint(1, 2)

                index = enemies.index(enemy)

                enemy_rect, collision_types = move(enemy, enemy_movement, tile_rects)

                enemy = pygame.Rect(enemy_rect.x - scroll[0], enemy_rect.y - scroll[1], 60, 60)

                if collision_types['bottom'] == True:
                    enemy_y_momentum = 0

                if player_rect.colliderect(enemy_rect) and not block:
                    player_rect = pygame.Rect(600, 800, 18, 27)
                    subs -= 2500
                    enemy_gen = False

                    pos = player_rect.centerx - scroll[0], player_rect.centery - scroll[1]

                    if player_flip:
                        particles.append([list(pos), [4, 0], random.randint(2, 5)])

                    else:
                        particles.append([list(pos), [-4, 0], random.randint(2, 5)])

                    for particle in particles:
                        particle[0][0] += particle[1][0]
                        particle[0][1] += particle[1][1]

                        particle[2] -= 0.1

                        particle[1][1] += 0.03

                        pygame.draw.circle(display, (255, 255, 255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))
                                    
                        if particle[2] <= 0:
                            particles.remove(particle)

                if enemy.collidepoint((bx, by)):
                    screen_shake = 1
                    destroy_bullet = True
                    destroy_sound.play()
                    enemies.pop(index)
                    enemies.append(pygame.Rect(random.randint(0, 960), random.randint(0, 480), 32, 32))
                    subs += 10000


                display.blit(enemy_image, enemy)

        if destroy_bullet:
            screen_shake = 1

            pos = bullet_rect.centerx, bullet_rect.centery

            if player_flip:
                particles.append([list(pos), [4, 0], random.randint(5, 5)])

            else:
                particles.append([list(pos), [-4, 0], random.randint(5, 5)])

            for particle in particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                particle[2] -= 0.1

                particle[1][1] += 0.03

                pygame.draw.circle(display, (255, 255, 255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))
                            
                if particle[2] <= 0:
                    particles.remove(particle)


        if len(enemies) < 20:
            enemies.append(pygame.Rect(random.randint(0, 960), random.randint(0, 480), 32, 32))

        # pygame.draw.rect(display, (255, 255, 255), (player_rect.x - scroll[0], player_rect.y - scroll[1], 18, 27))
        player_frame += 1

        if player_frame >= len(animation_database[player_action]):
            player_frame = 0


        player_image_id = animation_database[player_action][player_frame]
        
        player_image = animation_frames[player_image_id]

        player_image = pygame.transform.flip(player_image, player_flip, False)

        display.blit(player_image, ((player_rect.x - 8) - scroll[0], (player_rect.y - 3) - scroll[1]))
        centered_rotation(display, gun, gun_rect.topleft, -math.degrees(direction))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_menu = True
                    playing = False

                if event.key == K_d:
                    moving_right = True

                if event.key == K_a:
                    moving_left = True

                if event.key == K_SPACE:
                    if air_timer < 20:
                        player_y_momentum = -8.5
                        jump_sound.play()

                if event.key == K_w:
                    block = True

                if event.key == K_r:
                    player_rect = pygame.Rect(600, 800, 18, 27)

            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False

                if event.key == K_a:
                    moving_left = False

                if event.key == K_w:
                    block = False


            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and shoot_timer < 3:
                    shoot_sound.play()
                    shoot = True
                    shoot_timer = 0

            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and shoot_:
                    shoot_timer += 2

        if shoot_timer > 3:
            shoot_timer = 0

        for i in coin_pos:
            # i.x = i.x / (pygame.display.get_surface().get_size()[0] / 480)
            # i.y = i.y / (pygame.display.get_surface().get_size()[1] / 360) 

            display.blit(coin, (i.x - scroll[0], i.y - scroll[1]))

            if i.colliderect(player_rect):
                coin_pos.remove(i)
                subs += 5000

        if len(coin_pos) < 30:
            for i in range(2):
                coin_pos.append(pygame.Rect(random.randint(0, 1000), random.randint(0, 720), 32, 32))


        text("FPS: " + str(int(fps.get_fps())), (255, 255, 255), 16, 50, 45, font, display)
        text("Subs: " + str(int(subs)), (255, 255, 255), 16, 50, 70, font, display) 
        text("Sub Goal: 2,000,000", (255, 255, 255), 16, 50, 95, font, display) 

        upscaled_display = pygame.transform.scale(display, (pygame.display.get_surface().get_size()[0], pygame.display.get_surface().get_size()[1]))
        screen.blit(upscaled_display, (0, 0))

        if subs > sub_goal:
            screen.fill((0, 0, 0))
            text("bruh", (255, 255, 255), 60, pygame.display.get_surface().get_size()[0] / 2 - 50, pygame.display.get_surface().get_size()[1] / 2, font, screen)

        pygame.draw.circle(screen, (255, 255, 255), (mx, my), 4)

        pygame.display.update()
        fps.tick(60)
        




