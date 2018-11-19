slug_grav = 5
slug_speed = 5

size = width, height = 1000, 1000

data_dir = "./assets"


def calculate_orientation(orientation):
    if orientation == 0:
        gravity = (slug_grav,0)
        movepos = (0, -slug_speed)
    elif orientation == 1:
        gravity = (0,slug_grav)
        movepos = (slug_speed, 0)
    elif orientation == 2:
        gravity = (-slug_grav, 0)
        movepos = (0, slug_speed)
    elif orientation == 3:
        gravity = (0,-slug_grav)
        movepos = (-slug_speed,0)
    else:
        print("fuck")
        raise
    return gravity, movepos

