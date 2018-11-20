import pygame as pg
from graphics import *
from assets import *
from settings import *
from enum import Enum


class BackgroundSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        self.anim = background_animate(background_anim)
        self.image = pg.transform.scale(self.anim.next(), (height, width))
        self.rect = self.image.get_rect()
        # self.rect = (0,0)

    def animate(self):
        self.image = pg.transform.scale(self.anim.next(), (height, width))


    def update(self, dt):
        self.animate()

