import pygame as pg
from graphics import *
import pygame.gfxdraw
from assets import *
from settings import *
from enum import Enum

ATOM_IMG = pg.Surface((50, 50), pygame.SRCALPHA)
pygame.gfxdraw.aacircle(ATOM_IMG, 15, 15, 14, (0, 255, 0))
pygame.gfxdraw.filled_circle(ATOM_IMG, 15, 15, 14, (255, 0, 0))


class LaserState(Enum):
    WAITING = 0
    EXPLODING = 1
    EXPLODED = 2

class LaserSprite(pygame.sprite.Sprite):

    def __init__(self, init_location, orientation):
        pg.sprite.Sprite.__init__(self)
        self.state = LaserState.EXPLODING
        self.anim = bomb_animate(bomb_anim)
        self.image = pg.transform.scale2x(self.anim.next())
        self.orientation = orientation
        self.rect = self.image.get_rect(center=init_location)
        self.current_time = 0

    def on_hit(self, orientation, thing):
        pass

    def animate(self):
        self.image = pg.transform.scale2x(self.anim.next())
        self.image = reorient(self.orientation, self.image)

    def update(self, dt):
        self.current_time += dt
        self.animate()
        if self.current_time > 2 and self.state == LaserState.EXPLODING:
            create_laser_event = pg.event.Event(pg.USEREVENT, {"event_id": MyEvent.LASER_EXPLODING})
            self.anim = bomb_animate(explosion_anim)
            self.image = pg.transform.scale2x(self.anim.next())
            pg.event.post(create_laser_event)
            self.state = LaserState.EXPLODED
            self.current_time = 0
        if self.current_time > 0.75 and self.state == LaserState.EXPLODED:
            create_laser_event = pg.event.Event(pg.USEREVENT, {"event_id": MyEvent.LASER_EXPLODE})
            pg.event.post(create_laser_event)
            self.kill()

