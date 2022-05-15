import pygame as pg
from settings import *
from collision import collide_horizontal, collide_vertical
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
        self.direction = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(x, y)
        self.angle = 0
        self.last_shot = 0
        self.start_stunt = 0
        self.health = PLAYER_HEALTH

    def input(self, now):
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            self.rot_speed = PLAYER_ROT_SPEED
        elif keys[pg.K_k]:
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

        if keys[pg.K_SPACE]:
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                self.shot()

    def shot(self):
        dir = pg.math.Vector2(1, 0).rotate(-self.angle)
        pos = self.pos + BARREL_OFFSET.rotate(-self.angle)
        Bullet(self.game, pos, dir)
        MuzzleFlash(self.game, pos)

    def move(self):
        self.pos += self.direction * PLAYER_SPEED * self.game.dt

        self.hit_rect.centerx = self.pos.x
        collide_horizontal(self, self.game.walls,'slide')
        self.hit_rect.centery = self.pos.y
        collide_vertical(self, self.game.walls,'slide')
        self.rect.center = self.hit_rect.center

    def rotate(self):
        self.angle = (self.angle + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        now = pg.time.get_ticks()
        if now - self.start_stunt > STUNT_DURATION:
            self.input(now)

        self.rotate()
        self.move()
        

