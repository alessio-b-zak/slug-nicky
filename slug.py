import pygame as pg
from graphics import *
from assets import *
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
    IDLE = 4

class SlugSprite(pg.sprite.Sprite):
    def __init__(self, sprite_name, orientation):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.state = SlugState.IDLE
        self.prevstate = self.state
        self.lastwalkdir = None
        self.changed_state = False
        self.anim = None
        self.gravity, self.movepos = calculate_orientation(orientation)

    def apply_movement(self):
        if self.state == SlugState.MOVING_RIGHT:
            newpos = self.rect.move(*self.movepos)
            self.rect = newpos
        elif self.state == SlugState.MOVING_LEFT:
            newpos = self.rect.move(*(tuple(-1*x for x in self.movepos)))
            self.rect = newpos
        newpos =  self.rect.move(self.gravity)
        self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def calculate_state(self):
        keys = pg.key.get_pressed()
        self.prevstate = self.state
        if keys[pg.K_RIGHT]:
            self.state = SlugState.MOVING_RIGHT
        if keys[pg.K_LEFT]:
            self.state = SlugState.MOVING_LEFT
        if not (keys[pg.K_RIGHT] or keys[pg.K_LEFT]):
            self.state = SlugState.IDLE
        if not (self.state == self.prevstate):
            self.changed_state = False
        print(self.state)

    def animate_slug(self):
        if self.state == SlugState.MOVING_RIGHT and not self.changed_state:
            self.anim = default_animate(slug_walk)
            self.changed_state = True
            self.lastwalkdir = SlugState.MOVING_RIGHT
        if self.state == SlugState.MOVING_LEFT and not self.changed_state:
            self.anim = default_animate(slug_walk)
            self.changed_state = True
            self.lastwalkdir = SlugState.MOVING_LEFT
        if self.state == SlugState.IDLE and not self.changed_state:
            self.anim = default_animate(slug_idle)
            self.changed_state = True

        self.image = pg.transform.scale2x(self.anim.next())
        if (self.lastwalkdir == SlugState.MOVING_LEFT):
            self.image = pg.transform.flip(self.image, True, False)


    def update(self, dt):
        self.calculate_state()
        self.apply_movement()
        self.animate_slug()

