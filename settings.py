import pygame as pg
import math
from enum import Enum

slug_grav = 5
slug_speed = 5

bullet_speed = 2

size = width, height = 1500, 1500

data_dir = "./assets"


def move_to_point(origin, destination, fps):
    dx, dy = (destination[0] - origin[0], destination[1] - origin[1])
    stepx, stepy = (dx/fps , dy/fps )
    return stepx, stepy

class CollisionType(Enum):
    SLIME = 0
    BULLET = 1
    BOSS = 2
    LASER = 3

class MyEvent(Enum):
    CREATE_SLIME = 0
    FIRE_LASER = 1
    LASER_EXPLODING = 2
    LASER_EXPLODE = 3
    FIRE_CANNON = 4

orientation0_controls = (pg.K_s, pg.K_w, pg.K_d)
orientation1_controls = (pg.K_LEFT, pg.K_RIGHT, pg.K_UP)
orientation2_controls = (pg.K_u, pg.K_j, pg.K_k)
orientation3_controls = (pg.K_g, pg.K_f, pg.K_v)

def calculate_orientation(orientation):
    if orientation == 0:
        gravity = (slug_grav,0)
        movepos = (0, -slug_speed)
        controls = orientation0_controls
    elif orientation == 1:
        gravity = (0,slug_grav)
        movepos = (slug_speed, 0)
        controls = orientation1_controls
    elif orientation == 2:
        gravity = (-slug_grav, 0)
        movepos = (0, slug_speed)
        controls = orientation2_controls
    elif orientation == 3:
        gravity = (0,-slug_grav)
        movepos = (-slug_speed,0)
        controls = orientation3_controls
    else:
        print("fuck")
        raise
    return gravity, movepos, controls


def reorient(orientation, image):
    if (orientation == 0):
        image = pg.transform.rotate(image, 90)
    if (orientation == 2):
        image = pg.transform.rotate(image, -90)
    if (orientation == 3):
        image = pg.transform.rotate(image, 180)
    return image

def calc_opposite_orient(orientation):
    if (orientation == 0):
        return 2
    if (orientation == 1):
        return 3
    if (orientation == 2):
        return 0
    if (orientation == 3):
        return 1

def distance(source, target):
    dist = math.sqrt((target[1]-source[1])**2 + (target[0]-source[0])**2)
    return dist

class GameOverEnum(Enum):
    SNAILS = 0
    SLUGS = 1

