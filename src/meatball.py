import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        # self.state_gen = itertools.cycle(
        #     [
        #         child for child in self.init["children"] 
        #         if child["id"] == "animation"
        #     ]
        #     [0]["animation"].keys()
        # )
        self.move = Movement(self.sprite)
        self.state = "stage1"
        self.cur_action = 4
    
    def update(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) > 1000:
            self.last_time = cur_time
            self.cur_action = random.choice(list(range(5)))
        
        if self.cur_action == 4:
            return
        else:
            self.move(self.cur_action, speed=25)
            # self.move(self.cur_action+random.choice([-1,1]), speed=25)
            self.move(self.cur_action+1, speed=25)


