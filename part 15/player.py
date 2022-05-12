import pygame as pg
from settings import *
from collision import collide_with_walls
from bullet import Bullet
from muzzleflash import MuzzleFlash

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        self.vel = pg.math.Vector2(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = pg.math.Vector2(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = pg.math.Vector2(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = pg.math.Vector2(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = pg.math.Vector2(-KICKBACK, 0).rotate(-self.rot)
                MuzzleFlash(self.game, pos)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
