import pygame as pg
from graphics import *
from assets import *
from settings import *
from enum import Enum
from spriteanim import *

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
    IDLE = 4

class SlugSprite(pg.sprite.Sprite):
    def __init__(self, sprite_name, orientation):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.state = SlugState.IDLE
        self.prevstate = self.state
        self.started_anim = False
        self.anim = None
        self.gravity, self.movepos = calculate_orientation(orientation)

    def calculate_movement(self):
        keys = pg.key.get_pressed()
        self.prevstate = self.state
        if keys[pg.K_RIGHT]:
            newpos = self.rect.move(*self.movepos)
            self.rect = newpos
            self.state = SlugState.MOVING_RIGHT
        if keys[pg.K_LEFT]:
            newpos = self.rect.move(*(tuple(-1*x for x in self.movepos)))
            self.rect = newpos
            self.state = SlugState.MOVING_LEFT
        if not (keys[pg.K_RIGHT] or keys[pg.K_LEFT]):
            self.state = SlugState.IDLE
        if not (self.state == self.prevstate):
            self.started_anim = False
        newpos =  self.rect.move(self.gravity)
        self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def animate_slug(self):
        if self.state == SlugState.MOVING_RIGHT and not self.started_anim:
            slug_walk = data_dir + "/" + slug_sprite_walk_1
            self.anim = SpriteStripAnim(slug_walk, (0,0,93,93), 4, -1, True, 12)
            self.started_anim = True
        if self.state == SlugState.IDLE and not self.started_anim:
            slug_idle = data_dir + "/" + slug_sprite_idle_1
            self.anim = SpriteStripAnim(slug_idle, (0,0,93,93), 4, -1, True, 12)
            self.started_anim = True

        self.image = pg.transform.scale2x(self.anim.next())

    def update(self, dt):
        self.calculate_movement()
        self.animate_slug()

