import pygame as pg
import random
from graphics import *
from assets import *
from settings import *
from enum import Enum


class BossState(Enum):
    IDLE = 0
    FIRING = 1
    MOVING = 2



class BossSprite(pg.sprite.Sprite):
    def __init__(self, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        # self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.anim = boss_animate(boss_anim)
        self.image = pg.transform.scale2x(self.anim.next())
        self.aimed_position = self.gen_rand_position()
        self.moving = True
        self.epsilon = 10
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.state = BossState.IDLE
        self.prevstate = self.state
        self.lastwalkdir = None
        self.changed_state = False

    def gen_rand_position(self):
        return random.randint(0, width), random.randint(0, height)

    def apply_movement(self):
        # if self.moving:
        #     if (self.rect.center )
        pass

    def on_hit(self, orientation, collision_type):
        pass

    def animate(self):
        self.image = pg.transform.scale2x(self.anim.next())

    def update(self, dt):
        self.apply_movement()
        self.animate()
