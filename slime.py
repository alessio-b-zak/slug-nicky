import pygame as pg
from graphics import *
from assets import *
from settings import *
from enum import Enum


class BulletState(Enum):
    FIRING = 0
    HIT = 1
    EXPLODING = 2
    OFF_SCREEN = 3

class SlimeSprite(pg.sprite.Sprite):
    def __init__(self, orientation, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.orientation = orientation
        self.image = load_image(data_dir, slime_sprite, -1)
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.state = BulletState.FIRING
        self.gravity, _, _ = calculate_orientation(orientation)

    def apply_movement(self):
        newpos =  self.rect.move(self.gravity)
        self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def update(self, dt):
        self.apply_movement()
