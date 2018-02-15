# event_manager.py
from constants import *


class EventManager():

    def __init__(self, eng):
        self.eng    = eng
        self.logic = self.eng.lman
        

    def events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.eng.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.logic.left()
        if keys[pg.K_RIGHT]:
            self.logic.right()
        if keys[pg.K_UP]:
            self.logic.up()
        if keys[pg.K_DOWN]:
            self.logic.down()
        if not (keys[pg.K_LEFT]  or\
                keys[pg.K_RIGHT] or\
                keys[pg.K_UP]    or\
                keys[pg.K_DOWN]):
            self.logic.no_key()
        if keys[pg.K_BACKSPACE]:
            self.eng.running = False

