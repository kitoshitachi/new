# KidsCanCode - Game Development with pg video series
# Tile-based game - Part 15
# Simple Visual Effects (and a bug fix)
# Video link: https://youtu.be/ZapYMuV8f1g
from random import sample
import pygame as pg
import sys
from os import path
from settings import WHITE
from tilemap import *
from mob import Mob
from player import Player, Player1, Player2
from obstacle import Obstacle
from collision import collide_hit_rect
# HUD functions

class Level:
	def __init__(self,map_name):
		pg.init()
		self.screen = pg.display.get_surface()
		self.rect = self.screen.get_rect()
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		
		self.load_data(map_name)
		
	def load_data(self,map_name):
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		map_folder = path.join(game_folder, 'maps')
		self.map = TiledMap(path.join(map_folder, map_name))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
		self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
		self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
		self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
		self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
		self.gun_flashes = []
		for img in MUZZLE_FLASHES:
			self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())

	def new(self):
		# initialize all variables and do all the setup for a new game
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.walls = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.start = []
		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == 'player':
				# Player(self, tile_object.x, tile_object.y)
				self.start.append((tile_object.x,tile_object.y))
			if tile_object.name == 'zombie':
				Mob(self, tile_object.x, tile_object.y)
			if tile_object.name == 'wall':
				Obstacle(self, tile_object.x, tile_object.y,
						 tile_object.width, tile_object.height)
		self.camera_left = Camera(self.map.width, self.map.height)
		self.camera_right = Camera(self.map.width, self.map.height)
		self.draw_debug = False

	def create_player(self):
		pos_1,pos_2 = sample(self.start, 2)
		self.player = (Player1(self,pos_1[0],pos_1[1]),Player2(self,pos_2[0],pos_2[1]))

	def run(self):
		while True:
			self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
			self.events()
			self.update()
			self.draw()

	def quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		# update portion of the game loop
		self.all_sprites.update()
		self.camera_left.update(self.player[0])
		self.camera_right.update(self.player[1])
		# mobs hit player
		for player in self.player:
			hits = pg.sprite.spritecollide(player, self.mobs, False, collide_hit_rect)
			for hit in hits:
				player.health -= MOB_DAMAGE
				hit.vel = pg.math.Vector2(0, 0)
				if player.health <= 0:
					self.playing = False
			if hits:
				player.pos += pg.math.Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].angle)
		# bullets hit mobs
		hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
		for hit in hits:
			hit.health -= BULLET_DAMAGE
			hit.vel = pg.math.Vector2(0, 0)

	def draw(self):
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

		self.camera_left.surf.fill(BGCOLOR)
		self.camera_right.surf.fill(BGCOLOR)

		self.camera_left.surf.blit(self.map_img, self.camera_left.apply_rect(self.map_rect))
		self.camera_right.surf.blit(self.map_img, self.camera_right.apply_rect(self.map_rect))

		for sprite in self.all_sprites:
			if isinstance(sprite, Mob):
				sprite.draw_health()
			self.camera_left.surf.blit(sprite.image, self.camera_left.apply(sprite))
			self.camera_right.surf.blit(sprite.image, self.camera_right.apply(sprite))

			if self.draw_debug:
				pg.draw.rect(self.camera_left.surf, CYAN, self.camera_left.apply_rect(sprite.hit_rect), 1)
				pg.draw.rect(self.camera_right.surf, CYAN, self.camera_right.apply_rect(sprite.hit_rect), 1)

		if self.draw_debug:
			for wall in self.walls:
				pg.draw.rect(self.camera_left.surf, CYAN, self.camera_left.apply_rect(wall.rect), 1)
				pg.draw.rect(self.camera_right.surf, CYAN, self.camera_right.apply_rect(wall.rect), 1)

		self.draw_bar(self.camera_left.surf, 10, 10, self.player[0].health / PLAYER_HEALTH)
		self.draw_bar(self.camera_right.surf, WIDTH/2 + 10, 10, self.player[0].health / PLAYER_HEALTH)

		self.screen.fill(BGCOLOR)
		self.screen.blit(self.camera_left.surf, (0, 0))
		self.screen.blit(self.camera_right.surf, (WIDTH/2, 0))

		# pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
		# HUD functions
		pg.display.flip()

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

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				if event.key == pg.K_SPACE:
					self.draw_debug = not self.draw_debug

class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.SCALED | pg.FULLSCREEN)
		pg.display.set_caption('Magic Bullet')
		self.level = Level('level1.tmx')
		self.clock = pg.time.Clock()
		
	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
			self.level.new()
			self.level.create_player()
			self.level.run()

if __name__ == '__main__':
	game = Game()
	game.run()


