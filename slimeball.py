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

class BulletSprite(pg.sprite.Sprite):
    def __init__(self, sprite_name, orientation, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.rect = initial_position
        self.orientation = orientation
        self.state = BulletState.FIRING
        self.anim = None
        self.next_kill = False
        self.animating = False
        self.gravity, _, _ = calculate_orientation(orientation)
        self.gravity = tuple(-1*x for x in self.gravity)

    def apply_movement(self):
        if self.state == BulletState.OFF_SCREEN:
            self.kill()
        if self.state == BulletState.FIRING:
            newpos = self.rect.move(self.gravity)
            self.rect = newpos
        if is_off_screen(self.rect):
            self.state = BulletState.OFF_SCREEN

    def on_hit(self):
        self.state = BulletState.EXPLODING

    def animate(self):
        if self.state == BulletState.FIRING and not self.animating:
            self.anim = default_animate(bullet_anim)
            self.animating = True
        self.image = pg.transform.scale2x(self.anim.next())

    def update(self, dt):
        self.apply_movement()
        self.animate()

