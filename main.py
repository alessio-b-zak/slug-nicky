import pygame as pg
import sys
import os
from assets import *
from graphics import *

data_dir = "./assets"


class SlugSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(data_dir, slug_sprite, -1)
        self.gravity = (0, 2)
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            newpos = self.rect.move(10,0)
            self.rect = newpos
        if keys[pg.K_LEFT]:
            newpos = self.rect.move(-10, 0)
            self.rect = newpos
        newpos =  self.rect.move(gravity)
        self.rect = newpos

class Scene():
    def __init__(self):
        slug_sprite = SlugSprite()
        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(slug_sprite)
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.sprite_group.update()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
        self.sprite_group.draw(screen)



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
        'size':(600,400),
        'fps' :60
    }

    app = Game(**settings)
    app.main_game_loop()
    pg.quit()
    sys.exit()
