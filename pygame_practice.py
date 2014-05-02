import pygame
import math
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((640, 480))

FPS = 60
time = 0
clock = pygame.time.Clock()

class Vec2(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Ship(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('fighter.png').convert_alpha()
		self.size = 50
		self.angle = 0
		self.offset = Rect(0, 0, self.size, self.size)
		self.index = Vec2(0, 0)
		
		self.banks = True
		self.banking_right = False
		self.banking_left = False
		self.firing_engines = False
		self.engine_throttle = 0
		self.light_timer = 0

		self.pos = Vec2(15,15)

		self.rows = 24 if self.banks else 8


	def update(self, dt):
		idx = math.floor(self.angle / 5.625);

		self.index.x = math.floor(idx % 8);
		self.index.y = math.floor(idx / 8);

		if self.banks:
			if self.banking_right:
				self.index.y += 16
			if self.banking_left:
				self.index.y += 8

		if self.firing_engines:
			self.engine_throttle += dt * .2
		else:
			self.engine_throttle -= dt * .2

		if self.engine_throttle < 0:
			self.engine_throttle = 0
		if self.engine_throttle > 1:
			self.engine_throttle = 1

		self.light_timer += dt * .04
		if self.light_timer > 1:
			self.light_timer = 0

		if self.angle > 359:
			self.angle = 0
		if self.angle < 0:
			self.angle = 359

	def draw(self, surface):
		sprite_x = self.index.x * self.size
		sprite_y = self.index.y * self.size

		if sprite_y > self.size * self.rows - self.size:
			sprite_y = 0

		surface.blit(self.image, (self.pos.x, self.pos.y), pygame.Rect(sprite_x, sprite_y, self.size, self.size))

	def forward(self, dt):
		term = (self.angle - 90) * (math.pi / 180)
		x_component = math.cos(term)
		y_component = math.sin(term)
		self.pos.x += x_component * 3
		self.pos.y += y_component * 3

		if self.pos.x > 640:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = 640

		if self.pos.y > 480:
			self.pos.y = 0
		if self.pos.y < 0:
			self.pos.y = 480

	def rotate_left(self, dt):
		self.angle -= dt * 15

	def rotate_right(self, dt):
		self.angle += dt * 15

s = Ship()
bg = pygame.image.load('stars.jpg').convert()

main_loop = True
while main_loop:
	milliseconds = clock.tick(FPS)

	dt = milliseconds / 100.0
	time += dt
	screen.blit(bg, (0,0))
	s.update(dt)
	s.draw(screen)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			main_loop = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				main_loop = False

			elif event.key == pygame.K_SPACE:
				pass

	keystate = pygame.key.get_pressed()
	if keystate[K_w]:
		s.forward(dt)
	if keystate[K_a]:
		s.rotate_left(dt)
		s.banking_left = True
	else:
		s.banking_left = False
	if keystate[K_d]:
		s.rotate_right(dt)
		s.banking_right = True
	else:
		s.banking_right = False

	pygame.display.set_caption("[FPS]: %.2f" % clock.get_fps())
	pygame.display.flip()