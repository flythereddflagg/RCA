import random
import math

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
        self.signals = []
        self.hp = 50


    def animate(self):
        super().animate()
        if self.animate_data['id'] == 'damage' and self.animation_active:
            self.move(self.direction, speed=-3*self.speed)

    def choose_action(self):
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_action_time > self.action_time: 
            self.last_action_time = cur_time
            self.action = random.choice(MOVEMENTS)
            self.action_time = random.randint(*ACTION_TIME_RANGE)

    def update(self):
        self.choose_action() # choose a random action
        self.check_collision() # update action if necessaary
        
        self.apply_action(self.action)
        self.check_signals()

        self.animate()
        

        if self.hp <= 0: 
            self.kill()


    def check_signals(self):
        if self.signals: print(f"[{self.id}] got signals:\n{self.signals}")
        for signal in self.signals:
            if "damage" in signal[0]:
                self.hp -= signal[1]
                self.direction = signal[2]
                self.animate_data = self.animation['damage']
                self.animation_active = not self.animate_data["repeat"]

        self.signals = [] # reset signals

    def signal(self, signal):
        self.signals.append(signal)

    def apply_action(self, action):
        if self.animation_active: return

        if action in Compass.strings: 
            # ^ means a direction button is being pressed
            self.move(action, speed=self.speed)
            self.direction = Compass.i_map[action]
            self.animate_data = self.animation['walk']
            
        elif action == "STOP":
            self.animate_data = self.animation["stand"]

        else:
            print(self, action + "! (no response)")
            return


    def check_collision(self):
        if self.animate_data['id'] == 'damage' and self.animation_active:
            return
        collided_players = pg.sprite.spritecollide(
            # collide between self and player
            self, self.scene.groups['player'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        )
        if collided_players is not None:
            for player in collided_players:
                player.signal([
                    'damage', 10, Compass.opposite[self.direction]
                ])
                
