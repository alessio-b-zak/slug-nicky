import pygame as pg
import sys
import os
from assets import *
from graphics import *
from settings import *
from slug import *
from slime import *
from slimeball import *

class Scene():
    def __init__(self):
        self.slug_sprite_group = pg.sprite.LayeredUpdates()
        self.bullet_sprite_group = pg.sprite.LayeredUpdates()
        self.slime_sprite_group = pg.sprite.LayeredUpdates()
        self.sprite_groups = [self.slug_sprite_group, self.bullet_sprite_group, self.slime_sprite_group]
        for i in range(0, 4):
            self.slug_sprite_group.add(SlugSprite(i))
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_1]:
                sprite_loc = self.slug_sprite_group.get_sprite(0).rect.center
                self.bullet_sprite_group.add(BulletSprite(0, sprite_loc))
            if keys[pg.K_2]:
                sprite_loc = self.slug_sprite_group.get_sprite(1).rect.center
                self.bullet_sprite_group.add(BulletSprite(1, sprite_loc))
            if keys[pg.K_3]:
                sprite_loc = self.slug_sprite_group.get_sprite(2).rect.center
                self.bullet_sprite_group.add(BulletSprite(2, sprite_loc))
            if keys[pg.K_4]:
                sprite_loc = self.slug_sprite_group.get_sprite(3).rect.center
                self.bullet_sprite_group.add(BulletSprite(3, sprite_loc))
        elif event.type == pg.USEREVENT:
            if event.dict["event_id"] == MyEvent.CREATE_SLIME:
                self.slime_sprite_group.add(SlimeSprite(event.dict["orientation"], event.dict["location"]))

    def update(self, screen, dt):
        for group in self.sprite_groups:
            group.update(dt)
        self.calculate_collisions()
        self.draw(screen)

    def calculate_collisions(self):
        collide_dict = pg.sprite.groupcollide(self.slug_sprite_group, self.bullet_sprite_group, False, False)
        if collide_dict:
            for key, value in collide_dict.items():
                if not key.orientation == value[0].orientation:
                    key.on_hit(value[0].orientation)
                    value[0].on_hit(key.orientation)

    def draw(self, screen):
        background_im, _ = load_image(data_dir, background)
        screen.blit(background_im, [0,0])
        for group in self.sprite_groups:
            group.draw(screen)

class Game:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
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
    settings = {
        'size':(width, height),
        'fps' :60
    }

    app = Game(**settings)
    app.main_game_loop()
    pg.quit()
    sys.exit()
