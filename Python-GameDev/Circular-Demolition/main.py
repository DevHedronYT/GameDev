import pygame,sys,time,math,random
from pygame.locals import *

# Using Python 3.9 and pygame==2.0.0


pygame.init()
pygame.mixer.init()

def menu(display):
		cursor_image = pygame.transform.scale(pygame.image.load('cursor.png').convert_alpha(), (32, 32))
		cursor_image.set_colorkey((0, 0, 0))
		clock=pygame.time.Clock()
		play=pygame.Rect(width/2-170,height/2-100,250,50)
		exit=pygame.Rect(width/2-170,height/2,250,50)
		pygame.mouse.set_visible(False)

		click_sound=pygame.mixer.Sound('sounds/click.wav')
		click_sound.set_volume(0.75)
		class Circle:
			def __init__(self,x,y,radius,color,angle,distance_from_center,curve):
				self.x=x
				self.y=y
				self.r=radius
				self.color=color
				self.angle=angle
				self.discent=distance_from_center
				self.curve=curve
			def draw(self):
				pygame.draw.circle(display,self.color,(self.x,self.y),self.r)
				self.x=self.discent*self.curve*math.cos(self.angle)+width/2
				self.y=self.discent*self.curve*math.sin(self.angle)+height/2-25
				self.angle+=0.01
		circles=[]
		draw=True
		click = False
		while True:
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				elif event.type==MOUSEBUTTONDOWN:
					click=True
				elif event.type==MOUSEBUTTONUP:
					click=False



			display.fill((0,0,0))
			
			pygame.draw.rect(display,(0,0,0),play)
			pygame.draw.rect(display,(0,0,0),exit)
			if draw:
				for i in range(20):
					circles.append(Circle(width/2,height/2,40,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),math.radians(random.randint(0,360)),random.randint(100,500),1))
			draw=False
			for i in circles:
				i.draw()
			mx,my=pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.xquit()
					sys.exit()
			if play.collidepoint((mx,my)):
				if click:
					click_sound.play()
					main()
			elif exit.collidepoint((mx,my)):
				if click:
					click_sound.play()
					pygame.quit()
					sys.exit()
		
			mx,my=mouse_pos = pygame.mouse.get_pos()
			display.blit(cursor_image,(mx-15,my-15))


			display.blit(font.render('PLAY',True,(255,255,255)),(width/2-80,height/2-90))
			display.blit(font.render('EXIT',True,(255,255,255)),(width/2-80,height/2))
			pygame.display.update()
			clock.tick(120)


size=pygame.display.Info()
width=size.current_w - 100
height=size.current_h - 100
font=pygame.font.Font('font/cour.ttf',32)
display=pygame.display.set_mode((width,height), DOUBLEBUF)

pygame.display.set_caption("Circular Demolition")

pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.075)


def main():
	
	
	dt=time.time()-time.time()
	
	difficulty=1 #Change this for difficulty easy:1 medium:2 hard:3 very hard :4
#To chnage the player back to white remove lines 168
	
	
	
	class Player:
		def __init__(self,x,y,radius,speed,color):
			self.x=x
			self.y=y
			self.r=radius
			self.s=speed
			self.v=[0,0] #v refers to velocity
			self.color=color
			
		def draw(self):
			pygame.draw.circle(display,self.color,(self.x,self.y),self.r)
			
		def update_v(self):
			self.v[0],self.v[1]=0,0
			key=pygame.key.get_pressed()
			if key[K_UP] or key[K_w]:
				self.v[1]=-self.s
			if key[K_DOWN] or key[K_s]:
				self.v[1]=self.s
			if key[K_LEFT] or key[K_a]:
				self.v[0]=-self.s
			if key[K_RIGHT] or key[K_d]:
				self.v[0]=self.s
			
		def update(self):
			self.update_v()
			self.x+=self.v[0]*dt
			self.y+=self.v[1]*dt
			if self.x<=0:
				self.x=width
			elif self.x>=width:
				self.x=0
			elif self.y<=0:
				self.y=height
			elif self.y>=height:
				self.y=0
	
	class Jet:
		def __init__(self,x,y,velocity,radius):
			self.ex,self.ey=hedron.x,hedron.y #ex refers to x pos of enemy
			self.x=x
			self.y=y
			self.size=radius
			self.color=(random.random()*255,random.random()*255,random.random()*255)
			self.v=velocity
			
		def draw(self):
			
			pygame.draw.circle(display,self.color,(self.x,self.y),self.size)
			
			ang=math.atan2(self.ey-self.y,self.ex-self.x)
			self.x+=math.cos(ang)*self.v*dt
			self.y+=math.sin(ang)*self.v*dt
			self.ex=hedron.x
			self.ey=hedron.y
	
	class Bullet:
		def __init__(self,radius,velocity):
			self.x=hedron.x
			self.y=hedron.y
			self.r=radius
			self.v=velocity
			self.color=hedron.color
		def draw(self):
			pygame.draw.circle(display,self.color,(self.x,self.y),self.r)
			self.x+=self.v[0]*10*dt
			self.y+=self.v[1]*10*dt
			self.color=hedron.color #line only in use when player changes its color
	
	class Particle:
		def __init__(self,x,y,color):
			self.x=x
			self.y=y
			self.color=color
			self.size=random.randint(1,4)
			self.time=3
			self.vx=random.randrange(-10,10)
			self.vy=random.randrange(-10,10)
		def draw(self):
				pygame.draw.circle(display,self.color,(self.x,self.y),self.size)
				self.x+=self.vx
				self.y+=self.vy
				self.time-=0.1
	
	class ExpandCircle:
				def __init__(self,x,y,color):
					self.x=x
					self.y=y
					self.color=color
					self.r=10
					self.w=20
					self.chance=random.randint(1,10)
					self.time=4
				def draw(self):
					pygame.draw.circle(display,self.color,(self.x,self.y),self.r,self.w)
					if self.chance<9:
						self.w+=20
						self.r+=5
					else:
						self.w=3
						self.r+=5
						self.time-=0.2
				
	hedron=Player(width/2,height/2,25,5,(255,255,255))
	
	clock=pygame.time.Clock()
	last_time=time.time()
	
	jets=[]
	particles=[]
	bullets=[]
	game_over=False
	click=False
	Expand=[]
	restart=pygame.Rect(width/2-200,height/2-60,400,50)
	exit=pygame.Rect(width/2-200,height/2+20,400,50)
	points=0
	screen_stimer=0 #Screen shake timer
	pos=[0,0] #pos for screen
	screen_shake = False
	pygame.mouse.set_visible(False)


	cursor_image = pygame.transform.scale(pygame.image.load('cursor.png').convert_alpha(), (32, 32))
	cursor_image.set_colorkey((0, 0, 0))
	
	shoot_sound=pygame.mixer.Sound('sounds/projectile.wav')
	explosion_sound=pygame.mixer.Sound('sounds/explosion.wav')
	click_sound=pygame.mixer.Sound('sounds/click.wav')
	
	click_sound.set_volume(0.75)
	shoot_sound.set_volume(0.35)
	explosion_sound.set_volume(0.25)
	
	while True:
		
		display.fill((0,0,0))

		hedron.update()
		hedron.draw()
		
		for jet in jets:
			jet.draw()
			if math.hypot(hedron.x-jet.x,hedron.y-jet.y)-jet.size-hedron.r<-5:
				game_over=True
			for bullet in bullets:
				if math.hypot(bullet.x-jet.x,bullet.y-jet.y)-jet.size-bullet.r<0:
					if jet.size>25:
						for i in range(40):
							jet.size-=0.1
					else:
						if jet in jets and bullet in bullets:
							Expand.append(ExpandCircle(jet.x,jet.y,jet.color))
							for i in range(20):
								particles.append(Particle(bullet.x,bullet.y,jet.color))
							jets.remove(jet)
							bullets.remove(bullet)
							explosion_sound.play()
							points+=1
							screen_stimer+=1
				
		for particle in particles:
			particle.draw()
			particle.size-=0.1
			if particle.time<=0:
				particles.remove(particle)
			
		for c in Expand:
			c.draw()
			if c.chance<9:
				if c.w >=190:
					Expand.remove(c)
			else:
				if c.time<=0:
					Expand.remove(c)
			
		for bullet in bullets:
			bullet.draw()
			if bullet.x>width or bullet.x<-10 or bullet.y>height or bullet.y<-10:
				bullets.remove(bullet)
		
		dt=time.time()-last_time
		dt*=60
		last_time=time.time()
		
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==MOUSEBUTTONDOWN:
				click=True
			elif event.type==MOUSEBUTTONUP:
				click=False
		
		#Game over setup
		if game_over:
			color=(random.random()*225,random.random()*255,random.random()*255)
			while True:
				display.fill((0, 0, 0))
				pygame.draw.rect(display,(78,97,114),(width/2-250,height/2-125,500,250),0,100)
				pygame.draw.rect(display,(95,150,179),restart,0,100)
				pygame.draw.rect(display,(95,150,179),exit,0,100)
				display.blit(font.render('RESTART',True,(68,87,94)),(exit.x+140,exit.y-70))
				display.blit(font.render('EXIT',True,(68,87,94)),(exit.x+160,exit.y+5))
				display.blit(font.render(f'HEDRON KILLS {points} JETS',True,color),(width/2-190,height/2-125))
				for event in pygame.event.get():
					if event.type==QUIT:
						click_sound.play()
						pygame.quit()
						sys.exit()
					if event.type==MOUSEBUTTONDOWN:
						if event.button == 1:
							click_sound.play()
							x,y=pygame.mouse.get_pos()
							if exit.collidepoint((x,y)):
								menu(display)
							if restart.collidepoint((x,y)):
								main()
				mx, my = pygame.mouse.get_pos()
				display.blit(cursor_image,(mx-15,my-15))
				pygame.display.update()
				clock.tick(60)
		#Bullets setup
		if click:
			shoot_sound.play()
			mx,my=pygame.mouse.get_pos()
			angle=math.atan2(my-hedron.y,mx-hedron.x)
			velocity=[math.cos(angle),math.sin(angle)]
			bullets.append(Bullet(5,velocity))
			hedron.color=(random.random()*225,random.random()*255,random.random()*255)#remove this line
			
			if len(bullets) >= random.randint(50, 100):
				click = False

			
		# Screen shake Setup
		if screen_stimer>=150 and screen_stimer <=185:
			pos=[random.randint(-7,7),random.randint(-7,7)]
			screen_shake = True
		elif screen_stimer>150:
			screen_stimer=0
			pos=[0,0]
			screen_shake = False
		
		#Enemies setup
		if len(jets) <= 30:
			radius=random.randint(10,40)
			x,y=0,0
			if random.random()<0.5:
				if random.random()<0.5:
					x=0-radius
				else:
					x=width+radius
				y=random.random()*height
			else:
				if random.random()<0.5:
					y=0-radius
				else:
					y=radius+height
				x=random.random()*width
			
			jets.append(Jet(x,y,difficulty,radius))
		
	#	if hedron.y >= height:
	#		hedron.y = 0 

	#	elif hedron.y <= -height:
	#		hedron.y = height
		 
		display.blit(font.render(f'FPS {round(clock.get_fps())}',True,(88,107,114)),(10,10))
		display.blit(font.render(f'POINTS {points}',True,(108,128,134)),(width/2-120,10))
		mx,my=mouse_pos = pygame.mouse.get_pos()
		display.blit(cursor_image,(mx-15,my-15))
		if screen_shake:
			display.blit(display,pos, None, special_flags=BLEND_RGB_ADD)
		pygame.display.update()
		clock.tick(120)
menu(display)
main()
