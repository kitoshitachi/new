import pygame as pg
from settings import *
from collision import collide_horizontal, collide_vertical, collide_hit_rect
from bullet import Bullet
from muzzleflash import MuzzleFlash


class Player(pg.sprite.Sprite):
	def __init__(self, level, x, y):
		self._layer = PLAYER_LAYER
		self.groups = level.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.level = level
		self.image = level.player_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.hit_rect = PLAYER_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.direction = pg.math.Vector2(0, 0)
		self.pos = pg.math.Vector2(x, y)
		self.angle = 0
		self.last_shot = 0
		self.start_stunt = 0
		self.health = PLAYER_HEALTH

	def shot(self):
		dir = pg.math.Vector2(1, 0).rotate(-self.angle)
		pos = self.pos + BARREL_OFFSET.rotate(-self.angle)
		Bullet(self.level, pos, dir)
		MuzzleFlash(self.level, pos)

	def move(self):
		self.pos += self.direction * PLAYER_SPEED * self.level.dt

		self.hit_rect.centerx = self.pos.x
		collide_horizontal(self, self.level.walls,'slide')
		self.hit_rect.centery = self.pos.y
		collide_vertical(self, self.level.walls,'slide')
		self.rect.center = self.hit_rect.center

	def rotate(self):
		self.angle = (self.angle + self.rot_speed * self.level.dt) % 360
		self.image = pg.transform.rotate(self.level.player_img, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def collide_mob(self):
		hits = pg.sprite.spritecollide(self, self.level.mobs, False, collide_hit_rect)
		for hit in hits:
			self.health -= MOB_DAMAGE
			hit.vel = pg.math.Vector2(0, 0)

	@staticmethod
	def draw_bar(surf, x, y, pct):
		if pct < 0:
			pct = 0
		BAR_LENGTH = 100
		BAR_HEIGHT = 20
		fill = pct * BAR_LENGTH
		outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
		if pct > 0.6:
			col = GREEN
		elif pct > 0.3:
			col = YELLOW
		else:
			col = RED
		pg.draw.rect(surf, col, fill_rect)
		pg.draw.rect(surf, WHITE, outline_rect, 2)


	def update(self):
		now = pg.time.get_ticks()
		if now - self.start_stunt > STUNT_DURATION:
			self.input(now)

		self.rotate()
		self.collide_mob()
		self.move()


class Player1(Player):
	def input(self, now):
		self.rot_speed = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_g]:
			self.rot_speed = PLAYER_ROT_SPEED
		elif keys[pg.K_h]:
			self.rot_speed = -PLAYER_ROT_SPEED

		if keys[pg.K_w]:
			self.direction.y = -1
		elif keys[pg.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0
		
		if keys[pg.K_a]:
			self.direction.x = -1
		elif keys[pg.K_d]:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if self.direction.magnitude() != 0:
			self.direction.normalize_ip()

		if keys[pg.K_j]:
			if now - self.last_shot > BULLET_RATE:
				self.last_shot = now
				self.shot()

class Player2(Player):
	def input(self, now):
		self.rot_speed = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_i]:
			self.rot_speed = PLAYER_ROT_SPEED
		elif keys[pg.K_o]:
			self.rot_speed = -PLAYER_ROT_SPEED

		if keys[pg.K_UP]:
			self.direction.y = -1
		elif keys[pg.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0
		
		if keys[pg.K_LEFT]:
			self.direction.x = -1
		elif keys[pg.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if self.direction.magnitude() != 0:
			self.direction.normalize_ip()

		if keys[pg.K_p]:
			if now - self.last_shot > BULLET_RATE:
				self.last_shot = now
				self.shot()