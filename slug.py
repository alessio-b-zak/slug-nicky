import pygame as pg
from graphics import *
from assets import *
from settings import *
from enum import Enum


class SlugState(Enum):
    MOVING_LEFT = 0
    MOVING_RIGHT = 1
    JUMPING = 2
    FIRING = 3
    IDLE = 4
    DYING = 5

class SlugSprite(pg.sprite.Sprite):
    def __init__(self, orientation, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        # self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.anim = slug_animate(slug_idle_small)
        self.image = pg.transform.scale2x(self.anim.next())
        self.encumbered_timer = 0
        self.encumbered = False
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.state = SlugState.IDLE
        self.shot_timer = 0
        self.prevstate = self.state
        self.orientation = orientation
        self.lastwalkdir = None
        self.changed_state = False
        self.gravity, self.movepos, self.controls = calculate_orientation(orientation)
        self.left_key = self.controls[0]
        self.right_key = self.controls[1]
        self.fire_key = self.controls[2]

    def apply_movement(self):
        if not self.encumbered:
            if self.state == SlugState.MOVING_RIGHT:
                newpos = self.rect.move(*self.movepos)
                self.rect = newpos
            elif self.state == SlugState.MOVING_LEFT:
                newpos = self.rect.move(*(tuple(-1*x for x in self.movepos)))
                self.rect = newpos
        else:
            if self.state == SlugState.MOVING_RIGHT:
                newpos = self.rect.move(*(tuple(0.5*x for x in self.movepos)))
                self.rect = newpos
            elif self.state == SlugState.MOVING_LEFT:
                newpos = self.rect.move(*(tuple(-(0.5)*x for x in self.movepos)))
                self.rect = newpos

        newpos =  self.rect.move(self.gravity)
        self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def calculate_state(self):
        keys = pg.key.get_pressed()
        self.prevstate = self.state
        if keys[self.right_key]:
            self.state = SlugState.MOVING_RIGHT
        if keys[self.left_key]:
            self.state = SlugState.MOVING_LEFT
        if not (keys[self.right_key] or keys[self.left_key]):
            self.state = SlugState.IDLE
        if not (self.state == self.prevstate):
            self.changed_state = False

    def on_hit(self, orientation, collision_type):
        if collision_type == CollisionType.SLIME:
            self.encumbered = True
        if collision_type == CollisionType.LASER:
            self.state = SlugState.DYING
            self.changed_state = False

    def animate(self):
        if self.state == SlugState.MOVING_RIGHT and not self.changed_state:
            self.anim = slug_animate(slug_walk_small)
            self.changed_state = True
            self.lastwalkdir = SlugState.MOVING_RIGHT
        if self.state == SlugState.MOVING_LEFT and not self.changed_state:
            self.anim = slug_animate(slug_walk_small)
            self.changed_state = True
            self.lastwalkdir = SlugState.MOVING_LEFT
        if self.state == SlugState.IDLE and not self.changed_state:
            self.anim = slug_animate(slug_idle_small)
            self.changed_state = True
        if self.state == SlugState.DYING and not self.changed_state:
            self.anim = slug_death(slug_die_anim)
            self.changed_state = True
        try:
            self.image = pg.transform.scale2x(self.anim.next())
            if (self.lastwalkdir == SlugState.MOVING_LEFT):
                self.image = pg.transform.flip(self.image, True, False)
            self.image = reorient(self.orientation, self.image)
        except:
            self.kill()


    def check_fire(self):
        keys = pg.key.get_pressed()
        if keys[self.fire_key]:
            fire_event_create = pg.event.Event(pg.USEREVENT, {"event_id": MyEvent.FIRE_CANNON, "location": self.rect.center, "orientation": self.orientation})
            pg.event.post(fire_event_create)
            self.shot_timer = 0

    def update(self, dt):
        self.shot_timer += dt
        if self.encumbered:
            self.encumbered_timer += dt
            if self.encumbered_timer > 1:
                self.encumbered = False
                self.encumbered_timer = 0
        if self.state != SlugState.DYING:
            self.calculate_state()
            self.apply_movement()
        if self.shot_timer > 1:
            self.check_fire()
        self.animate()
