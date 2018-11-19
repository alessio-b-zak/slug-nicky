import pygame as pg
import sys
import os

data_dir = "./assets"


slug_sprite = "slug_sprite.png"

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()




class Scene():
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
        image,_ = load_image(slug_sprite, -1)
        screen.blit(image, (0,0))



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
