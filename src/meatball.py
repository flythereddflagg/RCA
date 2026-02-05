import itertools

import pygame as pg

from .node import Node

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        self.state_gen = itertools.cycle(
            [
                child for child in self.init["children"] 
                if child["id"] == "animation"
            ]
            [0]["animation"].keys()
        )
    
    def update(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) > 3000:
            self.state = next(self.state_gen)
            print(self.state)
            self.last_time = cur_time

