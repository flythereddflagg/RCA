import random
import math

import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .animation import Animation
from .tools import list_collided


MOVEMENTS = Compass.strings + ['STOP', 'STOP', "STOP"]
ACTION_TIME_RANGE = [200, 1000]

class Dragon(Decal):
    def __init__(self, **options):
        super().__init__(**options)
        self.sprite = self
        self.move = Movement(self, **self.options)
        self.animation = Animation(
            self, self.options['animations'], self.options["path_prefix"]
        )
        self.action_time = 0
        self.last_action_time = 0
        self.action = None
        self.speed = 200 # pixels per second
        self.signals = []
        self.hp = 50
        self.damage_direction = pg.math.Vector2(0,1)
        self.state = "stand"

    def apply_physics(self):
        
        if self.state == 'damage' and self.animation.active:
            self.move(self.damage_direction, speed=3*self.speed)

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
        self.animation.update()
        self.apply_physics()
        

        if self.hp <= 0: 
            self.kill()


    def check_signals(self):
        if self.signals: print(f"[{self.id}] got signals:\n{self.signals}")
        for signal in self.signals:
            if "damage" in signal[0]:
                self.hp -= signal[1]
                self.damage_direction = signal[2]
                self.state = 'damage'

        self.signals = [] # reset signals

    def signal(self, signal):
        self.signals.append(signal)

    def apply_action(self, action):
        if self.animation.active: return

        if action in Compass.strings: 
            # ^ means a direction button is being pressed
            self.move(action, speed=self.speed)
            self.direction = Compass.index(action)
            self.state = 'walk'
            
        elif action == "STOP":
            self.state = "stand"

        else:
            print(self, action + "! (no response)")
            return


    def check_collision(self):
        if self.state == 'damage' and self.animation.active:
            return

        for player in list_collided(self, self.scene.groups['player']):
            if (player.animation and\
                player.animation.current['id'] == 'damage' and\
                player.animation.active
            ): continue

            damage_direction = (
                pg.math.Vector2(player.rect.center) -
                pg.math.Vector2(self.rect.center)
            ).normalize()
            player.signal([
                'damage', 10, damage_direction
            ])
            
