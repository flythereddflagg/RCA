# event_manager.py
import pygame as pg
from constants import *


class EventManager():

    def __init__(self, engine=None):
        self.engine = engine

    def capture_events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.plr.move(5,W)
        if keys[pg.K_RIGHT]:
            self.plr.move(5,E)
        if keys[pg.K_UP]:
            self.plr.move(5,N)
        if keys[pg.K_DOWN]:
            self.plr.move(5,S)
        if not (keys[pg.K_LEFT] or\
                keys[pg.K_RIGHT] or\
                keys[pg.K_UP] or\
                keys[pg.K_DOWN]):
            self.plr.stand()
        if keys[pg.K_BACKSPACE]:
            self.running = False

