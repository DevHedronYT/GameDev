import pygame, random, math, sys
from pygame.locals import * 
from traceback import print_exc

# Using Python 3.9.1 and pygame==2.0.1

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font, size)

    surface.blit(fonts[size].render(text, False, color), (x, y))

def collision_test(rect, tiles):
    return [tile for tile in tiles if rect.colliderect(tile)]

def move(rect, movement, tiles):
    collision_types = {
        "top"     : False,
        "bottom"  : False,
        "right"   : False,
        "left"    : False
    }

    rect.x += movement[0]
    # hit_list = collision_test(rect, tiles)
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left 
            collision_types["right"] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True

    rect.y += movement[1]
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

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
        animation_image = pygame.image.load(img_loc).convert()
        animation_frames[animation_frame_id] = animation_image.copy()

        for i in range(frame):
            animation_frame_data.append(animation_frame_id)


        n += 1

    return animation_frame_data

def change_action(action_var, frame, new_val):
    if action_var != new_val:
        action_var = new_val
        frame = 0

    return action_var, frame


def centered_rotation(surf, image, topleft, angle, colorkey):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image.set_colorkey(colorkey)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

size = (640, 480)
screen = pygame.display.set_mode(size, RESIZABLE)
display = pygame.Surface((512, 384))

pygame.display.set_caption("W1nter")

fps = pygame.time.Clock()

font = "files/font/m6x11.ttf"

tile_image = pygame.image.load("files/images/tile.png").convert()
tile_size = 32

pygame.display.set_icon(tile_image)

map_num = 0
game_map = load_map("map_" + str(map_num))
load = False
map_done = False

animation_database = {}

animation_database["idle"] = load_animation("files/images/player/idle/", [20, 20], "idle")
animation_database["run"] = load_animation("files/images/player/run/", [17, 17], "run")
animation_database["jump"] = load_animation("files/images/player/idle/", [20], "idle")

gun = pygame.image.load("files/images/gun.png").convert()

player_action = "idle"
player_frame = 0
player_flip = False
player_reset = False

dash = False
dash_timer = 0

moving_right = False
moving_left = False

shoot = False
bullet_move = False
bx, by = 0, 0
direction = None

player_y_momentum = 0

player_rect = pygame.Rect(200, 200, 28, 28)

air_timer = 0
shoot_timer = 0

shoot_ = 0

destroy_bullet = False

true_scroll = [0, 0]

block = False

click = False

enemy_image = pygame.image.load("files/images/enemy.png").convert()
enemies = []

y = 0
for row in game_map:
    x = 0
    for tile in row:
        if tile == "4":
            enemies.append(pygame.Rect(x * tile_size, y * tile_size, 32, 32))

        x += 1

    y += 1

timer = 0

particles = []

screen_shake = 0
shake_timer = 0

in_menu = True
playing = False

stamina = 2
stamina_images = [pygame.image.load("files/images/player/stamina/stamina_empty.png").convert(), pygame.image.load("files/images/player/stamina/stamina_half.png").convert(), pygame.image.load("files/images/player/stamina/stamina_full.png").convert()]
stamin_refill_timer = 450

coin_image = pygame.image.load("files/images/coin.png").convert() 
coin_count = 0
coin_rects = []
coins_length = 0
required_coins = 1

y = 0
for row in game_map:
    x = 0
    for tile in row:
        if tile == "3":
            coin_rects.append(pygame.Rect(x * tile_size, y * tile_size, 32, 32))

        x += 1

    y += 1

endgame_tiles = []
over = False

time = 0

click_sound = pygame.mixer.Sound('files/music/click.wav')
jump_sound = pygame.mixer.Sound('files/music/jump.wav')
hurt_sound = pygame.mixer.Sound('files/music/hurt.wav')

click_sound.set_volume(0.4)
jump_sound.set_volume(0.4)
hurt_sound.set_volume(0.4)

pygame.mixer.music.load("files/music/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.08)

while True:
    while in_menu:
        display.fill((0, 0, 0))

        display_size = (pygame.display.get_surface().get_size()[0], pygame.display.get_surface().get_size()[1])
        mx, my = pygame.mouse.get_pos()[0] / (display_size[0] / 512), pygame.mouse.get_pos()[1] / (display_size[1] / 384)

        play_button = pygame.Rect(size[0] / 2 - 145, size[1] / 2 - 80, 150, 40) 
        quit_button = pygame.Rect(size[0] / 2 - 145, size[1] / 2, 150, 40)

        if play_button.collidepoint((mx, my)):
            if click:
                click_sound.play()
                playing = True
                in_menu = False

        if quit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        text("Play", (255, 255, 255), 35, play_button.x + 45, play_button.y, font, display)    
        text("Quit", (255, 255, 255), 35, quit_button.x + 45, quit_button.y, font, display)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.circle(display, (255, 255, 255), (mx, my), 5)

        screen.blit(pygame.transform.scale(display, pygame.display.get_surface().get_size()), (0, 0))

        pygame.display.update()
        fps.tick(120)

    while playing:
        screen.fill((0, 0, 0))
        display.fill((0, 0, 0))

        display_size = (pygame.display.get_surface().get_size()[0], pygame.display.get_surface().get_size()[1])
        mouse_pos = pygame.mouse.get_pos()[0] / (display_size[0] / 512), pygame.mouse.get_pos()[1] / (display_size[1] / 384)

        true_scroll[0] += (player_rect.x - true_scroll[0] - 260) / 10
        true_scroll[1] += (player_rect.y - true_scroll[1] - 195) / 10

        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile != "0" and tile != "3" and tile != "4" and tile != "5":                
                    display.blit(tile_image, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
                    tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))

                x += 1

            y += 1

        player_movement = [0, 0]

        if moving_right:
            player_movement[0] += 3
            
        if moving_left:
            player_movement[0] -= 3

        if dash and dash_timer < 5 and stamina >= 0:
            jump_sound.play()
            if player_flip:
                player_movement[0] -= 25

            else:
                player_movement[0] += 25

            
            stamin_refill_timer = 450
            dash_timer += 1

        if stamina < 0:
            stamina = -1

        if stamina < 1:
            stamin_refill_timer -= 1

            if stamin_refill_timer <= 0:
                stamina += 1
                stamin_refill_timer = 450


        if stamina > 0 and stamina < 2:
            stamin_refill_timer -= 1

            if stamin_refill_timer <= 0:
                stamina += 1
                stamin_refill_timer = 450

        player_movement[1] += player_y_momentum
        player_y_momentum += 0.25

        if player_y_momentum >= 3:
            player_y_momentum = 3

        if player_movement[0] > 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "run")
            player_flip = False

        if player_movement[0] < 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "run")
            player_flip = True

        if player_movement[1] < 0:
            player_action, player_frame = change_action(player_action, player_frame, "jump")

            if player_movement[0] < 0:
                player_flip = True

            else:
                player_flip = False

        if air_timer > 20:
            player_action, player_frame = change_action(player_action, player_frame, "jump")

        if player_movement[0] == 0 and player_movement[1] == 0 and air_timer == 0:
            player_action, player_frame = change_action(player_action, player_frame, "idle")

        for i in coin_rects:
            display.blit(coin_image, (i.x - scroll[0], i.y - scroll[1]))

            if i.colliderect(player_rect):
                coins_length += 1
                coin_rects.remove(i)
                stamin_refill_timer -= 50
                coin_count += 1
                click_sound.play()

        for i in enemies:
            display.blit(enemy_image, (i.x - scroll[0], i.y - scroll[1]))

            if i.colliderect(player_rect):
                player_reset = True
                hurt_sound.play()

        for i in endgame_tiles:
            if i.colliderect(player_rect):
                over = True

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if load:
            if map_num > 9:
                map_num = 9

            game_map = load_map("map_" + str(map_num))

            player_reset = True
            del enemies[:]

            y = 0
            for row in game_map:
                x = 0
                for tile in row:
                    if tile == "3":
                        coin_rects.append(pygame.Rect(x * tile_size, y * tile_size, 32, 32))
                        required_coins += 1

                    if tile == "4":
                        enemies.append(pygame.Rect(x * tile_size, y * tile_size, 32, 32))   
                    
                    if tile == "5":
                        endgame_tiles.append(pygame.Rect(x * tile_size, y * tile_size, 32, 32))

                    x += 1

                y += 1

            load = False

        if coin_count == required_coins:
            required_coins = 0
            coin_count = 0
            map_done = True

        if player_reset:
            player_rect = pygame.Rect(200, 200, 32, 32)
            player_reset = False

        if map_done:
            map_num += 1
            load = True
            map_done = False

        if collisions["bottom"]:
            player_y_momentum = 0
            air_timer = 0

        else:
            air_timer += 0.25

        if air_timer > 320:
            player_rect.x, player_rect.y = 200, 200
            air_timer = 0

        if collisions["top"]:
            player_y_momentum += 2

        player_frame += 1

        if player_frame >= len(animation_database[player_action]):
            player_frame = 0


        player_image_id = animation_database[player_action][player_frame]
        
        player_image = animation_frames[player_image_id]
        player_image = pygame.transform.flip(player_image, player_flip, False)

        display.blit(player_image, ((player_rect.x) - scroll[0], (player_rect.y) - scroll[1]))

        for event in pygame.event.get():
            if event.type == KEYDOWN and over:
                player_rect.x, player_rect.y = 200, 200
                map_num = 0
                load = True
                over = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False
                    in_menu = True

                if event.key == K_d or event.key == K_RIGHT:
                    moving_right = True
                
                if event.key == K_a or event.key == K_LEFT:
                    moving_left = True

                if event.key == K_SPACE or event.key == K_UP:
                    if air_timer < 15:
                        jump_sound.play()
                        player_y_momentum = -6.5

                if event.key == K_s or event.key == K_DOWN:
                    if dash_timer < 3:
                        stamina -= 1
                        dash = True

                if event.key == K_r:
                    player_rect = pygame.Rect(200, 200, 32, 32)

            if event.type == KEYUP:
                if event.key == K_d or event.key == K_RIGHT:
                    moving_right = False

                if event.key == K_a or event.key == K_LEFT:
                    moving_left = False

                if event.key == K_s or event.key == K_DOWN:
                    dash = False
                    dash_timer = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text("FPS: " + str(int(fps.get_fps())), (255, 255, 255), 20, 40, 30, font, display)
        text("Coins: " + str(int(coin_count)) + "/" + str(required_coins), (255, 255, 255), 20, 390, 80, font, display)

        time += 1/fps.get_fps()
        text("Time: " + str(round(time, 3)), (255, 255, 255), 20, 390, 100, font, display)

        if stamina > -1:
            display.blit(pygame.transform.scale(stamina_images[stamina], (3 * 15, 15)), (430, 50))

        if over:
            display.fill((0, 0, 0))
            text("You Finished the Game!", (255, 255, 255), 35, display_size[0] / 2 - 190, display_size[1] / 2 - 60, font, display)


        pygame.draw.circle(display, (255, 255, 255), mouse_pos, 5)

        upscaled_display = pygame.transform.scale(display, display_size)
        screen.blit(upscaled_display, (0, 0))

        pygame.display.update()
        fps.tick(120)
