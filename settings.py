import pygame as pg


slug_grav = 5
slug_speed = 5

size = width, height = 1000, 1000

data_dir = "./assets"


orientation0_controls = (pg.K_s, pg.K_w)
orientation1_controls = (pg.K_LEFT, pg.K_RIGHT)
orientation2_controls = (pg.K_u, pg.K_j)
orientation3_controls = (pg.K_c, pg.K_x)

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

