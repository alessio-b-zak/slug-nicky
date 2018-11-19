import pygame as pg
import sys



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
