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
    def __init__(self, orientation, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.orientation = orientation
        self.anim = bullet_animate(bullet_anim_small)
        self.image = pg.transform.scale2x(self.anim.next())
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.enem_orient = None
        self.state = BulletState.FIRING
        self.next_kill = False
        self.animating = True
        self.gravity, _, _ = calculate_orientation(orientation)
        self.gravity = tuple(-bullet_speed*x for x in self.gravity)

    def apply_movement(self):
        if self.state == BulletState.OFF_SCREEN:
            self.kill()
        if self.state == BulletState.FIRING:
            newpos = self.rect.move(self.gravity)
            self.rect = newpos
        if is_off_screen(self.rect):
            self.state = BulletState.OFF_SCREEN

    def on_hit(self, orientation, collision_type):
        if not self.state == BulletState.EXPLODING:
            self.state = BulletState.EXPLODING
            self.enem_orient = orientation
            self.animating = False

    def animate(self):
        if self.state == BulletState.FIRING and not self.animating:
            self.anim = bullet_animate(bullet_anim_small)
            self.animating = True
        if self.state == BulletState.EXPLODING and not self.animating:
            self.anim = bullet_explode_animate(bullet_explode_anim)
            self.animating = True

        try:
            self.image = pg.transform.scale2x(self.anim.next())
        except:
            if not self.enem_orient == -1:
                create_slime_event = pg.event.Event(pg.USEREVENT,{"event_id": MyEvent.CREATE_SLIME, "orientation": self.enem_orient, "location": self.rect.center})
                pg.event.post(create_slime_event)
            self.kill()

    def update(self, dt):
        self.apply_movement()
        self.animate()
