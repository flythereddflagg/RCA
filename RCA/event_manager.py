# event_manager.py
from constants import *


class EventManager():

    def __init__(self, eng):
        self.eng = eng
        self.player = self.eng.player
        

    def events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.eng.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.player.move(5,W)
        if keys[pg.K_RIGHT]:
            self.player.move(5,E)
        if keys[pg.K_UP]:
            self.player.move(5,N)
        if keys[pg.K_DOWN]:
            self.player.move(5,S)
        if not (keys[pg.K_LEFT] or\
                keys[pg.K_RIGHT] or\
                keys[pg.K_UP] or\
                keys[pg.K_DOWN]):
            self.player.stand()
        if keys[pg.K_BACKSPACE]:
            self.eng.running = False

