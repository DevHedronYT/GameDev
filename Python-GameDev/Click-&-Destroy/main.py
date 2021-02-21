import pygame, random, math, sys
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font, size)

    surface.blit(fonts[size].render(text, False, color), (x, y))

def col_gen():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def swap(surf, old_c, new_c):
    img_copy = pygame.Surface((31, 31))
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))

    return img_copy

class Enemy:
    def __init__(self, surface, color, pos, radius):
        self.surface = surface
        self.color = color
        self.pos = pos
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 255), self.pos, self.radius + 1)
        pygame.draw.circle(self.surface, self.color, self.pos, self.radius)

# size = (640, 480)
size = (960, 600)
screen = pygame.display.set_mode(size, RESIZABLE)
# display = pygame.Surface((320, 240))
display = pygame.Surface((400, 250))

window_size = pygame.display.get_surface().get_size()

pygame.display.set_caption("Destroy")

black = (0, 0, 0)
white = (255, 255, 255)

fps = pygame.time.Clock()

circle = pygame.image.load("assets/circle.png").convert()
circle = swap(circle, white, (49, 51, 53))

pygame.display.set_icon(circle)

enemies = []
for i in range(0, 30):
    enemies.append(Enemy(display, col_gen(), [random.randint(40, 280), random.randint(40, 240)], random.randint(11, 20)))

# enemies.append(Enemy(display, white, [200, 200], 10))  
# enemies.append(Enemy(display, (255, 0, 0), [100, 100], 20))

biggest_circle = None

click = False

particles = []

mouse_img = pygame.image.load("assets/crosshair.png").convert()
mouse_img.set_colorkey(black)

screen_shake = 0

timer = 0
timer_two = 0

score = 0

font = "assets/hfont.ttf"

explosion = pygame.mixer.Sound("assets/exp.wav")
comb = pygame.mixer.Sound("assets/exp_2.wav")

pygame.mixer.music.load("assets/music.wav")
pygame.mixer.music.play(-1)

death_timer = 2400

playing = True
dead = False

while True:
    while playing and not dead: 
        screen.fill(black)
        display.fill(black)

        display_size = pygame.display.get_surface().get_size()

        mouse_pos = pygame.mouse.get_pos()[0] / (pygame.display.get_surface().get_size()[0] / 400), pygame.mouse.get_pos()[1] / (pygame.display.get_surface().get_size()[1] / 250)

        for enemy in enemies:
            circ = pygame.transform.scale(circle, (int(enemy.radius) + 2, int(enemy.radius) + 2))
            circ.set_colorkey(black)
            display.blit(circ, enemy.pos)
            enemy.draw()
            
        
            # Rotate an object around another one

            if biggest_circle == None:
                biggest_circle = enemy
            
            if biggest_circle.radius < enemy.radius:
                biggest_circle = enemy

            if enemy.radius < biggest_circle.radius: 
                distx = enemy.pos[0] - biggest_circle.pos[0]
                disty = enemy.pos[1] - biggest_circle.pos[1]
        
                angle = math.atan2(disty, distx)    

                if enemy.pos.copy()[0] + enemy.radius > 400:
                    enemy.pos[0] = 0
                
                if enemy.pos.copy()[0] - enemy.radius < 0:
                    enemy.pos[0] = 320

                if enemy.pos.copy()[1] - enemy.radius > 250:
                    enemy.pos[1] = 0

                if enemy.pos.copy()[1] + enemy.radius < 0:
                    enemy.pos[1] = 240


                enemy.pos[0] += math.sin(angle) * 0.5 
                enemy.pos[1] -= math.cos(angle) * 0.5 

            for i in enemies:
                xdif = enemy.pos[0] - i.pos[0]
                ydif = enemy.pos[1] - i.pos[1]
                i_dist = math.sqrt((xdif ** 2) + (ydif ** 2))

                timer += 1

                if timer > 40000 and i_dist < enemy.radius and enemy.radius > i.radius or timer > 40000 and i_dist < enemy.radius and enemy.radius > i.radius and enemy.color == i.color:
                    comb.play()
                    enemy.radius += i.radius
                    enemies.remove(i)
                    for i in range(0, 4):
                        particles.append([enemy.pos.copy(), [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 13), enemy.color])
                    timer = 0


            if click:
                xdif = enemy.pos[0] - mouse_pos[0]
                ydif = enemy.pos[1] - mouse_pos[1]
                dis = math.sqrt((xdif ** 2) + (ydif ** 2))  

                if dis < enemy.radius:
                    screen_shake = 20
                    explosion.play()
                    if enemy.radius > 10:
                        enemy.radius = enemy.radius * 0.5
                        enemies.append(Enemy(display, enemy.color, [enemy.pos[0] + random.randint(-3, 3) * enemy.radius, enemy.pos[1] + random.randint(-3, 3) * enemy.radius], enemy.radius))

                        for i in range(0, 4):
                            particles.append([enemy.pos.copy(), [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 13), enemy.color])
                    score += enemy.radius

                    if enemy.radius <= 10: 
                        pos = enemy.pos.copy()
                        color = enemy.color

                        enemies.remove(enemy)

                        for i in range(0, 4):
                            particles.append([pos, [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 13), color])
                        if random.randint(0, 10000) < 100:
                            enemies.append(Enemy(display, col_gen(), [random.randint(40, 280), random.randint(40, 240)], random.randint(11, 20)))     


                biggest_circle = None

            # Add proper updating, movement, orbiting
            # Add combination
            # Add destruction
            # Add particles

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            particle[2] -= 0.1

            pygame.draw.circle(display, particle[3], (int(particle[0][0]), int(particle[0][1])), particle[2])

            if particle[2] <= 0:
                particles.remove(particle)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if screen_shake > 0:
            screen_shake -= 1

        render_offset = [0, 0]
        if screen_shake:
            render_offset[0] = random.randint(0, 8) - 4
            render_offset[1] = random.randint(0, 8) - 4

        if len(enemies) < 13:
            for i in range(0, 19):
                enemies.append(Enemy(display, col_gen(), [random.randint(40, 280), random.randint(40, 240)], random.randint(11, 20)))

        timer_two += 1

        if timer_two > 1800:
            for i in range(0, 10):
                enemies.append(Enemy(display, col_gen(), [random.randint(40, 280), random.randint(40, 240)], random.randint(11, 20)))
            timer_two = 0

        if biggest_circle is not None and biggest_circle.radius > 70:
            text("Warning, Hostile Alert", white, 20, 70, 30, font, display)

            sec_time = int(death_timer / 120)
            text("You have " + str(sec_time) + " seconds to destroy it", white, 17, 18, 225, font, display) 

            store = biggest_circle.pos.copy()
            pygame.draw.circle(display, white, store, 6)
            pygame.draw.circle(display, (255, 0, 100), store, 4)

            death_timer -= 1

        else:
            death_timer = 2400

        if death_timer == 0:
            dead = True
            playing = False

        text("Score: " + str(int(score)), white, 20, 30, 10, font, display)
        display.blit(mouse_img, (mouse_pos[0] - 15.5, mouse_pos[1] - 15.5))
        screen.blit(pygame.transform.scale(display, display_size), render_offset)

        pygame.display.update()
        fps.tick(120)
        

    while dead and not playing:
        screen.fill(black)
        text("You have didn't destroy the threat", white, 40, 18, 200, font, screen)
        text("in time as it was getting stronger", white, 40, 23, 240, font, screen)
        text("together...:/", white, 40, 23, 280, font, screen)
        text("Your score was: " + str(int(score)), white, 40, 23, 360, font, screen)
        text("Press any key to continue....", white, 40, 23, 420, font, screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                playing = True
                dead = False
                
                particles.clear()
                enemies.clear()

                screen_shake = 0

                timer = 0
                timer_two = 0


                biggest_circle = None

                click = False


                score = 0

        pygame.display.update()
        fps.tick(120)

