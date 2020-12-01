import pygame
import random
import sys
import math
import time
from pygame.locals import *

# Using python 3.8.5 and pygame==2.0.0.dev12
radius = random.randint(1, 100)
time_count = 0
materials = {}

def survive(player_mats, string):
    sentence = " ".join(player_mats)
    new_sentence = sentence.split(" ")

    count = 0
    index = 0
    animal_count = 0

    for i in new_sentence:
        count += 1
        if i == string:
            index = count - 2
            animal_count = new_sentence[index]

    return animal_count

def explore(radius, time_count, materials):
    diameter = radius * 2
    circumference = 3.14 * diameter
    area = 3.14 * (radius**2)

    if circumference < 50 and area < 50:
        time_count += 0

    if circumference > 50 and area > 50:
        time_count += 1

    materials = {
        "wood" : random.randint(210, 300),
        "leaves" : random.randint(210, 400),
        "fresh-water" : str(random.randint(10, 50)) + " Liters",
        "animals" : random.randint(8, 15) + 2
    }

    return time_count, materials

def harvest(materials, material):
    materials[material] = 0

    return materials[material]



island = list(explore(radius, time_count, materials))

time_took_to_travel = island[0]
island_mats = island[1]

pygame.init()

size = (1400, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyWeek 30')

fps = pygame.time.Clock()

running = True
in_menu = True
playing = False

game_font = pygame.font.Font('files/text.ttf', 40)
game_font2 = pygame.font.Font('files/text.ttf', 25)
game_font3 = pygame.font.Font('files/text.ttf', 23)
black = (0, 0, 0)
white = (255, 255, 255)

console_text = ""

commands = {"help" : "explore, harvest <material>, build raft, show-mats, time, eat, hunt, goal, escape(only works after making raft)"}

menu_bg_one = pygame.image.load('files/sprites/ocean_one.png').convert_alpha()
menu_bg_two = pygame.image.load('files/sprites/ocean_two.png').convert_alpha()

menu_bg_rect = menu_bg_one.get_rect(center = (32.5, 32.5))

menu_bg_one = pygame.transform.scale(menu_bg_one, (size[0], size[1]))
menu_bg_two = pygame.transform.scale(menu_bg_two, (size[0], size[1]))

menu_bgs = [menu_bg_one, menu_bg_two]

menu_bg_index = 0

click = False

game_bg_one = pygame.image.load('files/sprites/game_ocean_one.png').convert_alpha()
game_bg_two = pygame.image.load('files/sprites/game_ocean_two.png').convert_alpha()

game_bg_rect = game_bg_one.get_rect(center = (32.5, 32.5))
game_bg_one = pygame.transform.scale(game_bg_one, (550, size[1]))
game_bg_two = pygame.transform.scale(game_bg_two, (550, size[1]))

bgs = [game_bg_one, game_bg_two]

bg_index = 0

player_one = pygame.image.load('files/sprites/player_one.png').convert_alpha()

player_two = pygame.image.load('files/sprites/player_two.png').convert_alpha()

player_rect = player_one.get_rect(center = (400, 70))

player_sprites = [player_one, player_two]

player_sprite_index = 0

animation_duration = 500

frame_count = 0

console_arrow_rect_x, console_arrow_rect_y = 500, 20
console_text_rect_x, console_text_rect_y = console_arrow_rect_x + 10, 20

draw_again = False

again = False

output = game_font3.render("", True, white)

player_mats = ["0 animals"]

move_down_slow = False
move_down_fast = False

light_count = 0
night_count = 0

night = False

cursor_rect_x, cursor_rect_y = 510, console_text_rect_y

colors = [(52, 68, 86), white]

col_index = 0

hungry = False

num_of_animals = 0

animal_index = 0
animal_index2 = 0

hunger_capacity = 25000

have_eaten = False

have_eaten2 = True

die = False

hunger_capacity2 = 25000

raft = pygame.image.load('files/sprites/raft.png').convert_alpha()
raft = pygame.transform.scale2x(raft)
raft = pygame.transform.scale2x(raft)

draw_raft = False

index1 = 0
index2 = 0

away = False

reach_count = 50000

finish = False

draw_until_over = False

pygame.display.set_icon(raft)

click_sound = pygame.mixer.Sound('files/audio/click.wav')
#music = pygame.mixer.Sound('files/')

while running:

    while in_menu and playing != True:
        finish = False

        if menu_bg_index < 1:
            screen.fill((255, 255, 255))
            time.sleep(0.5)
            menu_bg_index += 1

        else:
            screen.fill((255, 255, 255))
            time.sleep(0.5)
            menu_bg_index = 0

        screen.blit(menu_bgs[menu_bg_index], menu_bg_rect)

        mx, my = pygame.mouse.get_pos()

        menu_text = game_font.render("Main Menu", True, black)
        play_text = game_font.render("Play Game", True, black)

        screen.blit(menu_text, (size[0] / 2 - 60, size[1] / 2 - 100))

        button = pygame.Rect(size[0] / 2 - 95, size[1] / 2, 200, 50)

        pygame.draw.rect(screen, white, button)
        screen.blit(play_text, (size[0] / 2 - 60, size[1] / 2))

        quit_text = game_font.render("Quit Game", True, black)
        button_2 = pygame.Rect(size[0] / 2 - 95, size[1] / 2 + 100, 200, 50)

        pygame.draw.rect(screen, white, button_2)
        screen.blit(quit_text, (size[0] / 2 - 60, size[1] / 2 + 100))

        if button.collidepoint((mx, my)):
            if click:
                in_menu = False
                playing = True
                screen.fill((0, 0, 0))
                click_sound.play()

        if button_2.collidepoint((mx, my)):
            if click:
                sys.exit()
                click_sound.play()

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

    while playing and in_menu != True and die != True:
        if away:
            bgs = [menu_bg_one, menu_bg_two]
            reach_count -= 10
            draw_until_over = True

            if reach_count < 0:
                finish = True
                playing = False

        else:
            playing = True
            finish = False
            bgs = [game_bg_one, game_bg_two]

        if island_mats['animals'] < 0:
            island_mats['animals'] = 0

        materials = "There are: " + str(island_mats['wood']) + " Wood, " + str(island_mats['leaves']) + " Leaves, " + str(island_mats['fresh-water']) + " of Fresh-Water & " + str(island_mats['animals']) + " animals "

        if bg_index < 2:
            screen.fill(white)
            bg_index += 0.04

        if bg_index > 2:
            screen.fill(white)
            bg_index = 0


        screen.blit(bgs[int(bg_index)], game_bg_rect)


        pygame.draw.line(screen, (72, 105, 131), (492, 0), (492, 800), 5)

        if night:
            screen.fill(black)

            night_text = game_font.render("It is night time", True, white)
            screen.blit(night_text, (size[0] / 2 - 490, size[1] / 2 - 100))

            light_count += 10

            time_until_day = game_font.render("Time left for day: " + str(light_count), True, white)
            screen.blit(time_until_day, (10, 750))

            if light_count > 10000:
                night = False
                night_count = 0

        console = pygame.Rect(495, 0, 1000, 800)
        pygame.draw.rect(screen, (52, 68, 86), console)

        help_text = game_font2.render("Type 'help' to get a list of commands and 'goal' to understand what you need to do", True, white)
        screen.blit(help_text, (console_arrow_rect_x, 5))

        fps_string = str(int(fps.get_fps()))
        fps_text = game_font.render("FPS: " + fps_string, True, white)
        screen.blit(fps_text, (10, 25))

        text_surface1 = game_font2.render("> ", True, white)

        screen.blit(text_surface1, (console_arrow_rect_x, console_arrow_rect_y))

        #pygame.draw.line(screen, (255, 255, 255), (console_text_rect_x + 10, console_text_rect_y + 20), (console_text_rect_x, console_text_rect_y + 20), 10)

        text_surface2 = game_font2.render(console_text, True, white)

        if player_sprite_index < 2:
            player_sprite_index += 0.05

        if player_sprite_index > 2:
            player_sprite_index = 0

        if draw_again:
            new = console_text.split(" ")

            if console_text == "goal":
                commands['goal'] = "You have to escape the island while battling hunger, using commands, and by building a raft"

            if draw_raft and away != True:
                if console_text == 'escape':
                    food = int(float(survive(player_mats, "animals")))

                    if food <= 0:
                        commands['escape'] = "Please get some food before continuing"

                    else:
                        commands['escape'] = "Escaping Island"
                        away = True


            if console_text == 'eat':
                num_of_animals_2 = survive(player_mats, "animals")

                if num_of_animals_2 == 0:
                    commands['eat'] = "You don't have any animals in your inventory, hunt to get animals"

                else:
                    have_eaten = True
                    num_of_animals_2 = float(num_of_animals_2)
                    num_of_animals_2 -= 0.25
                    if num_of_animals_2 < 0:
                        num_of_animals_2 = 0

                    if num_of_animals_2 == 0:
                        have_eaten = False
                    player_mats[0] = str(num_of_animals_2) + " animals"
                    commands['eat'] = "You have eaten 0.25 of one of the animals you hunted, you now have " + str(player_mats[0])



            if console_text == 'time':
                if night == False:
                    commands['time'] = "When the time in the bottom left becomes 100,000; it will be night"

                else:
                    commands['time'] = "When the time left in the bottom left becomes 10,000; it will be day"

            if night == False and away == False:
                if new[0] == 'build':

                    if console_text == 'build raft':

                        wood = survive(player_mats, "wood")
                        leaves = survive(player_mats, "leaves")

                        wood = int(wood) - 200
                        leaves = int(leaves) - 200


                        if wood > 0 and leaves > 0:
                            commands['build'] = "Building raft"
                            draw_raft = True

                        else:
                            commands['build'] = "Not Building raft due to not having enough materials, you need all the wood and all the leaves"
                            draw_raft = False


                if console_text == "hunt":
                    if island_mats['animals'] != 0:
                        num_of_animals = island_mats['animals']
                        nums_animals = survive(player_mats, "animals")
                        num_of_animals_you_hunt = random.randint(0, 2) + float(nums_animals)
                        island_mats['animals'] -=  num_of_animals_you_hunt


                        commands['hunt'] = "You have hunted " + str(num_of_animals_you_hunt) + " animal or animals in total"
                        player_mats[0] = str(num_of_animals_you_hunt) + " animals"

                        if time_count == 0:
                            move_down_slow = True
                            move_down_fast = False
                        else:
                            move_down_fast = True
                            move_down_slow = False

                    else:
                        commands['hunt'] = "No animals left"


                    #player_mats[index] = player_mats[index] + num_of_animals_you_hunt
                    #player_mats.append(str(num_of_animals_you_hunt) + " animals")


                if console_text == 'explore':
                    commands['explore'] = materials
                    if time_count == 0:
                        move_down_slow = True
                        move_down_fast = False
                    else:
                        move_down_fast = True
                        move_down_slow = False

                try:

                    if new[0] == 'harvest' and new[1] != 'animals' and island_mats[new[1]] != 0:
                        try:
                            harvesting = "You know have " + str(island_mats[console_text.split(" ")[1]]) + " " + new[1]
                            commands['harvest'] = harvesting
                            new_harvesting = harvesting.split("have ")
                            player_mats.append(new_harvesting[1])
                            island_mats[console_text.split(" ")[1]] = 0

                        except Exception as e:
                            output = game_font3.render("Invalid Command", True, white)

                        if time_count == 0:
                            move_down_slow = True
                            move_down_fast = False
                        else:
                            move_down_fast = True
                            move_down_slow = False

                    else:
                        output = game_font3.render("Invalid Command", True, white)

                except Exception as e:
                    output = game_font3.render("Invalid Command", True, white)


            if console_text == 'show-mats':
                try:
                    new_one = " ".join(player_mats)
                    commands['show-mats'] = "You have " + new_one

                except Exception as e:
                    output = game_font3.render("Invalid Command", True, white)

            try:
                output = game_font3.render(commands[new[0]], True, white)
            except Exception as e:
                output = game_font3.render("Invalid Command", True, white)

            again = True
            draw_again = False

        screen.blit(output, (console_arrow_rect_x, console_arrow_rect_y + 20))

        if again:
            console_text_rect_y += 30
            console_arrow_rect_y += 30

            #commands['harvest'] = console_text.split(' ')[1] "harvest" : "You know have " + island_mats[console_text.split(" ")[1]]
            console_text = ""

            screen.blit(text_surface1, (console_arrow_rect_x, console_arrow_rect_y))
            screen.blit(text_surface2, (console_text_rect_x, console_text_rect_y))

            again = False

        if move_down_slow:
            player_rect.centery += 10

        if move_down_fast:
            player_rect.centery += 20

        if console_arrow_rect_y > 600:
            console_arrow_rect_y = 20

        if console_text_rect_y > 600:
            console_text_rect_y = 20


        if player_rect.centery > 2000:
            move_down_fast = False
            move_down_slow = False
            player_rect.centery = 0

        if player_rect.centery != 70:
            player_rect.centery += 10

        night_count += 10

        if night_count > 90000 and night_count < 100000:
            hunt_text = game_font.render("Hunt before Night if you have not!", True, (255, 0, 0))
            screen.blit(hunt_text, (250, 400))

        if night_count > 100000:
            night = True

        if night == False:
            time_until_night = game_font.render("Time: " + str(night_count), True, white)
            screen.blit(time_until_night, (10, 750))

        screen.blit(text_surface2, (console_text_rect_x, console_text_rect_y))

        if cursor_rect_x < 510:
            cursor_rect_x = 510

        if cursor_rect_y > 600:
            cursor_rect_y = 20

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    click_sound.play()
                    draw_again = True
                    cursor_rect_y += 30
                    cursor_rect_x = 510

                if event.key == K_BACKSPACE:
                    console_text = console_text[:-1]
                    cursor_rect_x -= 10

                else:
                    cursor_rect_x += 10
                    console_text += event.unicode

                if event.key == K_ESCAPE:
                    playing = False
                    in_menu = True

        col_index += 0.1

        if draw_raft:
            screen.blit

        if col_index > 2:
            col_index = 0

        if hunger_capacity == 0 or hunger_capacity < 0 and have_eaten == False:
            hunger_capacity = 0
            eat_text = game_font.render("Hunt and then Eat or you will die", True, (255, 0, 0))
            screen.blit(eat_text, (30, 410))
            have_eaten2 = False

        if hunger_capacity > 0 and hunger_capacity != 0:
            hunger_capacity -= 10
            time_to_eat = game_font.render("Time until eating warning: " + str(hunger_capacity), True, white)
            screen.blit(time_to_eat, (500, 700))

        if have_eaten == True:
            hunger_capacity = 25000
            have_eaten2 = True
            have_eaten = False

        if have_eaten2 == True:
            hunger_capacity2 = 25000

        if have_eaten2 == False:
            hunger_capacity2 -= 10

            if hunger_capacity2 < 0:
                playing = False
                have_eaten = False
                hunger_capacity = 25000
                have_eaten2 = True
                night_count = 0
                light_count = 0
                player_mats = ["0 animals"]
                bgs = [game_bg_one, game_bg_two]
                island = list(explore(radius, time_count, materials))
                time_took_to_travel = island[0]
                island_mats = island[1]
                die = True


        if draw_raft:
            screen.blit(raft, (400 - 150, 70 - 20))

        screen.blit(player_sprites[int(player_sprite_index)], player_rect)

        pygame.draw.line(screen, colors[int(col_index)], (cursor_rect_x, cursor_rect_y), (cursor_rect_x, cursor_rect_y + 20), 5)

        if draw_until_over:
            time_until_finish = game_font.render("Time until reaching home: " + str(reach_count), True, white)
            screen.blit(time_until_finish, (10, 700))

        pygame.display.update()
        fps.tick(60)


    while finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                finish = False
                running = False
                sys.exit()

        screen.fill((0, 0, 0))
        play_again = game_font.render("Game Finished, Press any Key to quit", True, (255, 255, 255))
        screen.blit(play_again, (400, 400))

        pygame.display.update()
        fps.tick(60)

    while die:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                click_sound.play()
                die = False
                playing = True


        play_again = game_font.render("Dead, Press any key to play again", True, (255, 0, 0))
        screen.blit(play_again, (600, 400))

        pygame.display.update()
        fps.tick(60)
