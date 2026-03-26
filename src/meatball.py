import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        self.move = Movement(self.sprite, hitmask_sprite = self.hitmask.sprite)
        self.state = "stage1"
        self.cur_action = 4
    
    def update(self):
        player = self.scene.get_player().parent
        if player.inventory.contains("sword"):
            self.stage3()
            return
        elif player.inventory.contains("shovel"):
            self.state = "stage2"
        self.random_movement()

    def stage3(self):
        self.state = "wiggle"
        
    def random_movement(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) > 1000:
            self.last_time = cur_time
            self.cur_action = random.randint(0, 4)
        
        if self.cur_action == 4:
            return
        else:
            self.move(self.cur_action, speed=25)
            # self.move(self.cur_action+random.choice([-1,1]), speed=25)
            self.move(self.cur_action+1, speed=25)
            # self.move(3, speed=25)


