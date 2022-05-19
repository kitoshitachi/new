from random import choice, randrange
import pygame as pg
from settings import *
from collision import collide_horizontal, collide_vertical

class Mob(pg.sprite.Sprite):
	def __init__(self, level, x, y):
		self._layer = MOB_LAYER
		self.groups = level.all_sprites, level.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.level = level
		self.player = None
		self.image = level.mob_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.hit_rect = MOB_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.pos = pg.math.Vector2(x, y)
		self.direction = pg.math.Vector2(0, 0)
		self.acc = pg.math.Vector2(0, 0)
		self.rect.center = self.pos
		self.angle = 0
		self.health = MOB_HEALTH
		self.speed = choice(MOB_SPEEDS)
		self.mana = MOB_MANA
		self.start_rand = 0

	def avoid_mobs(self):
		for mob in self.level.mobs:
			if mob != self:
				dist = self.pos - mob.pos
				if 0 < dist.length() < AVOID_RADIUS:
					self.acc += dist.normalize()

	def move(self):
		self.acc = pg.math.Vector2(1, 0).rotate(-self.angle)
		self.avoid_mobs()
		self.acc.scale_to_length(self.speed)
		self.acc += self.direction * -1
		self.direction += self.acc * self.level.dt
		self.pos += self.direction * self.level.dt + 0.5 * self.acc * self.level.dt ** 2
		self.hit_rect.centerx = self.pos.x
		collide_horizontal(self, self.level.walls,'slide')
		self.hit_rect.centery = self.pos.y
		collide_vertical(self, self.level.walls,'slide')
		self.rect.center = self.hit_rect.center

	def on_sight(self):
		pass

	def rotate(self):
		
		self.image = pg.transform.rotate(self.level.mob_img, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def update(self):
		now = pg.time.get_ticks()
		if self.player != None:
			self.angle = (self.player.pos - self.pos).angle_to(pg.math.Vector2(1, 0))
		elif now - self.start_rand >= RAND_DURATION:
			self.start_rand = now
			self.angle = randrange(361)
		self.rotate()
		self.move()

		if self.health <= 0:
			self.kill()

	def draw_health(self):
		if self.health > 60:
			col = GREEN
		elif self.health > 30:
			col = YELLOW
		else:
			col = RED
		width = int(self.rect.width * self.health / MOB_HEALTH)
		self.health_bar = pg.Rect(0, 0, width, 7)
		if self.health < MOB_HEALTH:
			pg.draw.rect(self.image, col, self.health_bar)
