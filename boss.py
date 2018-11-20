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
    DYING = 4

class BossSprite(pg.sprite.Sprite):
    def __init__(self, initial_position):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        # self.image, self.rect = load_image(data_dir, sprite_name, -1)
        self.anim = boss_animate(boss_anim)
        self.image = pg.transform.scale2x(self.anim.next())
        self.aimed_position = self.gen_rand_position()
        self.orientation = -1
        self.last_person = None
        self.last_person_loc = None
        self.health = 20
        self.looking_left = False
        self.invul_timer = 0
        self.epsilon = 150
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.state = BossState.MOVING
        self.prevstate = self.state
        self.lastwalkdir = None
        self.changed_state = False

    def gen_rand_position(self):
        return random.randint(0+100, width-100), random.randint(0+100, height-100)

    def start_moving(self):
        self.state = BossState.MOVING

    def fire_laser(self):
        create_laser_event = pg.event.Event(pg.USEREVENT, {"event_id": MyEvent.FIRE_LASER})
        pg.event.post(create_laser_event)
        #take damage at point


    def apply_movement(self):
        if self.state == BossState.MOVING:
            if (distance(self.rect.center, self.aimed_position) < self.epsilon):
                self.state = BossState.FIRING
                self.aimed_position = self.gen_rand_position()
                self.fire_laser()
            else:
                point = move_to_point(self.rect.center, self.aimed_position, 60)
                if point[0] >= 0:
                    self.looking_left = True
                else:
                    self.looking_left = False
                newpos = self.rect.move(point)
                self.rect = newpos
        elif self.state == BossState.FIRING:
            self.looking_left = self.rect.center <= self.last_person_loc
            self.state = BossState.WAITING

    def on_hit(self, orientation, collision_type):
        if self.invul_timer > 0.5:
            self.health -= 1
            self.invul_timer = 0

    def animate(self):
        try:
            self.image = pg.transform.scale2x(self.anim.next())
            if (self.looking_left):
                self.image = pg.transform.flip(self.image, True, False)
        except:
            self.kill()

    def check_health(self):
        # print("Boss Health: " + str(self.health))
        if self.health <= 0 and self.state != BossState.DYING:
            self.state = BossState.DYING
            self.anim = snail_death(snail_die_anim)

    def update(self, dt):
        if self.state != BossState.DYING:
            self.apply_movement()
            self.invul_timer += dt
            self.check_health()
        self.animate()
