import pygame as pg
import sys
import os
from assets import *
from laser import *
from background import *
from graphics import *
from boss import *
from settings import *
from slug import *
from slime import *
from slimeball import *

class Scene():
    def __init__(self):
        self.background_sprite_group = pg.sprite.LayeredUpdates()
        self.boss_sprite_group = pg.sprite.LayeredUpdates()
        self.slug_sprite_group = pg.sprite.LayeredUpdates()
        self.bullet_sprite_group = pg.sprite.LayeredUpdates()
        self.slime_sprite_group = pg.sprite.LayeredUpdates()
        self.laser_sprite_group = pg.sprite.LayeredUpdates()
        self.sprite_groups = [self.background_sprite_group,self.boss_sprite_group, self.slug_sprite_group, self.bullet_sprite_group, self.slime_sprite_group, self.laser_sprite_group]
        # for i in range(0, 4):
        self.slug_sprite_group.add(SlugSprite(0, (width, height/2)))
        self.slug_sprite_group.add(SlugSprite(1, (width/2, height)))
        self.slug_sprite_group.add(SlugSprite(2, (0, height/2)))
        self.slug_sprite_group.add(SlugSprite(3, (width/2, 0)))
        self.boss_sprite = BossSprite((width/2, height/2))
        self.check_explode_collisions = False
        self.boss_sprite_group.add(self.boss_sprite)
        self.background_sprite_group.add(BackgroundSprite())

    def calculate_nearest(self):
        boss_sprite_loc = self.boss_sprite.rect.center
        min_dist = sys.maxsize
        min_pos = None
        nearest_orientation = None
        for slug in self.slug_sprite_group.sprites():
            dist = distance(boss_sprite_loc,slug.rect.center)
            if dist < min_dist:
                min_dist = dist
                min_pos = slug.rect.center
                nearest_orientation = slug.orientation
        return min_pos, nearest_orientation

    def get_event(self, event):
        if event.type == pg.USEREVENT:
            if event.dict["event_id"] == MyEvent.CREATE_SLIME:
                self.slime_sprite_group.add(SlimeSprite(event.dict["orientation"], event.dict["location"]))
            if event.dict["event_id"] == MyEvent.FIRE_LASER:
                if len(self.slug_sprite_group.sprites()) != 0:
                    nearest_loc, near_orientation = self.calculate_nearest()
                    if not self.boss_sprite.last_person == None:
                        if not self.boss_sprite.last_person == near_orientation:
                            self.laser_sprite_group.add((LaserSprite(nearest_loc)))
                            self.boss_sprite.last_person = near_orientation
                        else:
                            self.boss_sprite.start_moving()
                    else:
                        self.laser_sprite_group.add((LaserSprite(nearest_loc)))
                        self.boss_sprite.last_person = near_orientation
                    print(nearest_loc)
                    self.boss_sprite.last_person_loc = nearest_loc
            if event.dict["event_id"] == MyEvent.LASER_EXPLODING:
                self.check_explode_collisions = True
            if event.dict["event_id"] == MyEvent.LASER_EXPLODE:
                self.check_explode_collisions = False
                self.boss_sprite.start_moving()
            if event.dict["event_id"] == MyEvent.FIRE_CANNON:
                self.bullet_sprite_group.add(BulletSprite(event.dict["orientation"], event.dict["location"]))

    def update(self, screen, dt):
        for group in self.sprite_groups:
            group.update(dt)
        self.calculate_collisions()
        self.draw(screen)

    def calculate_collisions(self):
        #bullet slug collisions
        collide_dict = pg.sprite.groupcollide(self.slug_sprite_group, self.bullet_sprite_group, False, False)
        if collide_dict:
            for key, value in collide_dict.items():
                if not key.orientation == value[0].orientation:
                    key.on_hit(value[0].orientation, CollisionType.BULLET)
                    value[0].on_hit(key.orientation, CollisionType.BULLET)
        #slug slime collisions
        collide_dict = pg.sprite.groupcollide(self.slug_sprite_group, self.slime_sprite_group, False, False)
        if collide_dict:
            for key, value in collide_dict.items():
                key.on_hit(value[0].orientation, CollisionType.SLIME)
                value[0].on_hit(key.orientation, CollisionType.SLIME)
        #bullet boss collisions
        collide_dict = pg.sprite.groupcollide(self.boss_sprite_group, self.bullet_sprite_group, False, False)
        if collide_dict:
            for key, value in collide_dict.items():
                for bullet in value:
                    if bullet.state == BulletState.FIRING:
                        key.on_hit(value[0].orientation, CollisionType.BOSS)
                        bullet.on_hit(key.orientation, CollisionType.BOSS)
        #explosion slug collisions
        collide_dict = pg.sprite.groupcollide(self.slug_sprite_group, self.laser_sprite_group, False, False)
        if self.check_explode_collisions:
            if collide_dict:
                for key, value in collide_dict.items():
                    key.on_hit(value[0].orientation, CollisionType.LASER)
                    value[0].on_hit(key.orientation, CollisionType.LASER)

    def draw(self, screen):
        for group in self.sprite_groups:
            group.draw(screen)

class Game:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        pg.mixer.music.load(data_dir + "/" + song)
        pg.mixer.music.play()
        self.clock = pg.time.Clock()
        self.state = Scene()
    def update(self, dt):
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()

if __name__ == '__main__':
    pg.mixer.pre_init(44100, 16, 2, 4096)
    pg.init()
    settings = {
        'size':(width, height),
        'fps' :60
    }

    app = Game(**settings)
    app.main_game_loop()
    pg.quit()
    sys.exit()
