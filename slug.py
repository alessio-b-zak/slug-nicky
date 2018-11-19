import pygame as pg
from graphics import *
from settings import *
from enum import Enum

def calculate_orientation(orientation):
    if orientation == 0:
        gravity = (slug_grav,0)
        movepos = (0, slug_speed)
    elif orientation == 1:
        gravity = (0,slug_grav)
        movepos = (slug_speed, 0)
    elif orientation == 2:
        gravity = (-slug_grav, 0)
        movepos = (0, -slug_speed)
    elif orientation == 3:
        gravity = (0,-slug_grav)
        movepos = (-slug_speed,0)
    else:
        print("fuck")
        raise
    return gravity, movepos

class SlugState(Enum):
    MOVING_LEFT = 0
    MOVING_RIGHT = 1
    JUMPING = 2
    FIRING = 3

class SlugSprite(pg.sprite.Sprite):
    def __init__(self, sprite_name, orientation):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.gravity, self.movepos = calculate_orientation(orientation)
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            newpos = self.rect.move(*self.movepos)
            self.rect = newpos
        if keys[pg.K_LEFT]:
            newpos = self.rect.move(*(tuple(-1*x for x in self.movepos)))
            self.rect = newpos
        newpos =  self.rect.move(self.gravity)
        self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

