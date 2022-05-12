from random import uniform
import pygame as pg
from settings import *
from collision import collide_horizontal, collide_vertical,reflect

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir:pg.math.Vector2):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pg.math.Vector2(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.alive = 5

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x

        collide_horizontal(self, self.game.walls,'reflect')
        self.hit_rect.centery = self.pos.y
        collide_vertical(self, self.game.walls, 'reflect')

        if self.alive < 0:
            self.kill()
