import pygame as pg
import sys
import os
from assets import *
from graphics import *
from settings import *
from slug import *

class Scene():
    def __init__(self):
        self.sprite_group = pg.sprite.Group()
        for i in range(0, 4):
            self.sprite_group.add(SlugSprite(slug_sprite_char_1, i))
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.sprite_group.update(dt)
        self.draw(screen)
    def draw(self, screen):
        background_im, _ = load_image(data_dir, background)
        screen.blit(background_im, [0,0])
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
        'size':(width, height),
        'fps' :60
    }

    app = Game(**settings)
    app.main_game_loop()
    pg.quit()
    sys.exit()
