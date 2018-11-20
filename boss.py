import pygame as pg
import random
from graphics import *
from assets import *
from settings import *
from enum import Enum


class BossState(Enum):
    HURT = 0
    FIRING = 1
    MOVING = 2
    WAITING = 3

class BossSprite(pg.sprite.Sprite):
    def __init__(self, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        # self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.anim = boss_animate(boss_anim)
        self.image = pg.transform.scale2x(self.anim.next())
        self.aimed_position = self.gen_rand_position()
        self.last_person = None
        self.epsilon = 150
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.state = BossState.MOVING
        self.prevstate = self.state
        self.lastwalkdir = None
        self.changed_state = False

    def gen_rand_position(self):
        return random.randint(0, width), random.randint(0, height)

    def start_moving(self):
        print("made it in here")
        self.state = BossState.MOVING

    def fire_laser(self):
        print("created event")
        create_laser_event = pg.event.Event(pg.USEREVENT, {"event_id": MyEvent.FIRE_LASER})
        pg.event.post(create_laser_event)
        #take damage at point

    def apply_movement(self):
        if self.state == BossState.MOVING:
            if (distance(self.rect.center, self.aimed_position) < self.epsilon):
                self.state = BossState.FIRING
                self.aimed_position = self.gen_rand_position()
            else:
                newpos = self.rect.move(move_to_point(self.rect.center, self.aimed_position, 60))
                self.rect = newpos
        elif self.state == BossState.FIRING:
            print("firing")
            self.fire_laser()
            self.state = BossState.WAITING

    def on_hit(self, orientation, collision_type):
        pass

    def animate(self):
        self.image = pg.transform.scale2x(self.anim.next())

    def update(self, dt):
        self.apply_movement()
        self.animate()
