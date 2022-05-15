import pygame as pg

from settings import *

collide_hit_rect = lambda one,two: one.hit_rect.colliderect(two.rect)
NV = lambda x: -1 if x > 0 else 1

def slide(sprite,dir):
    if dir == 'x':
        sprite.direction.x = 0
    else:
        sprite.direction.y = 0

def reflect(sprite,NV):
    sprite.direction.reflect_ip(NV)
    if sprite.alive:
        sprite.alive -= 1

def collide_horizontal(sprite, group, respone):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if hits[0].rect.centerx > sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
        if hits[0].rect.centerx < sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
        sprite.hit_rect.centerx = sprite.pos.x
        if respone == 'slide':
            slide(sprite,'x')
        else:
            reflect(sprite,(NV(sprite.direction.x),0))


def collide_vertical(sprite,group, respone):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if hits[0].rect.centery > sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
        if hits[0].rect.centery < sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
        sprite.hit_rect.centery = sprite.pos.y
        if respone == 'slide':
            slide(sprite,'y')
        else:
            reflect(sprite,(0,NV(sprite.direction.y)))

