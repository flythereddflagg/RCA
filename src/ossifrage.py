import random

import pygame as pg
from .sprite import Character
from .compass import Compass

MOVEMENTS = Compass.strings + ['STOP', 'STOP', "STOP"]
ACTION_TIME_RANGE = [200, 1000]

class Ossifrage(Character):
    def __init__(self, **options):
        super().__init__(**options)
        self.action_time = 0
        self.last_action_time = 0
        self.action = None
        self.speed = 200 # pixels per second
        self.dist_per_frame = self.speed // self.game.FPS


    def update(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_action_time > self.action_time: 
            self.last_action_time = cur_time
            self.action = random.choice(MOVEMENTS)
            self.action_time = random.randint(*ACTION_TIME_RANGE)
        
        self.check_collision() # update action if necessaary
        
        self.apply_action(self.action)

        self.animate()


    def apply_action(self, action):
        if self.animation_active: return

        if action in Compass.strings: 
            # ^ means a direction button is being pressed
            self.move(Compass.vec_map[action], self.dist_per_frame)
            self.direction = Compass.i_map[action]
            self.animate_data = self.animation['walk']
            
        elif action == "STOP":
            self.animate_data = self.animation["stand"]

        else:
            print(self, action + "! (no response)")
            return


    def check_collision(self):
        if pg.sprite.spritecollide(
            # collide between character and foreground
            self, self.game.player, 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        ):
            pass
