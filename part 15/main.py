# KidsCanCode - Game Development with pg video series
# Tile-based game - Part 15
# Simple Visual Effects (and a bug fix)
# Video link: https://youtu.be/ZapYMuV8f1g
from random import sample
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from mob import Mob
from player import Player
from obstacle import Obstacle
from collision import collide_hit_rect
# HUD functions


class Level:
	def __init__(self,map_name):
		pg.init()
		self.screen = pg.display.set_mode()#set_mode((WIDTH, HEIGHT))
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
		# self.camera_right = Camera(self.map.width, self.map.height)
		self.draw_debug = False

	def create_player(self):
		pos = sample(self.start, 1)
		self.player = [Player(self,pos_x,pos_y) for pos_x,pos_y in pos]

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
		self.camera.update(self.player)
		# mobs hit player
		hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
		for hit in hits:
			self.player.health -= MOB_DAMAGE
			hit.vel = pg.math.Vector2(0, 0)
			if self.player.health <= 0:
				self.playing = False
		if hits:
			self.player.pos += pg.math.Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].angle)
		# bullets hit mobs
		hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
		for hit in hits:
			hit.health -= BULLET_DAMAGE
			hit.vel = pg.math.Vector2(0, 0)

	def draw(self):
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(BGCOLOR)
		self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
		for sprite in self.all_sprites:
			if isinstance(sprite, Mob):
				sprite.draw_health()
			self.screen.blit(sprite.image, self.camera.apply(sprite))
			if self.draw_debug:
				pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
		if self.draw_debug:
			for wall in self.walls:
				pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

		# pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
		# HUD functions
		#draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
		pg.display.flip()

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				if event.key == pg.K_h:
					self.draw_debug = not self.draw_debug

class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode()#(WIDTH, HEIGHT), pg.RESIZABLE | pg.SCALED)
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


