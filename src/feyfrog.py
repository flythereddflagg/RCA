import random
import math

import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .animation import Animation
from .tools import list_collided, vec, diff_vec


MOVEMENTS = Compass.strings + ['STOP', 'STOP', "STOP"]
ACTION_TIME_RANGE = [200, 1000]
DEFAULT_STATE = "stand"

class FeyFrog(Decal):

    def setup(self):
        super().setup()
        self.move = Movement(self, **self.init)
        self.action_time = 0
        self.last_action_time = 0
        self.action = None
        self.speed = 200 # pixels per second
        self.signals = []
        self.hp = 50
        self.damage_direction = vec((0,1))
        self.state = DEFAULT_STATE
        self.defualt_state = DEFAULT_STATE
        # random.seed(2343414142) # to make it determineistic


    def apply_physics(self):
        if self.state == 'damage' and self.animation.active:
            if self.ouch_fx.sound.get_num_channels() == 0:
                self.ouch_fx.play()
            self.move(self.damage_direction, speed=1*self.speed)


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
        self.apply_physics()
        

        if self.hp <= 0:
            sprite = self.scene.node_by_id("grate exit")
            sprite.set_image(
                pg.image.load("./assets/block/block.png").convert_alpha()
            )
            sprite.kill()
            self.scene.place_node(
                sprite,
                groups=["foreground"],
                start=self.scene.set_bg_pos(self.scene.game.get_center()),
                active=True
            )
            self.kill()


    def check_signals(self):
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

        for player in list_collided(
            self.hitmask.sprite, 
            self.scene.groups.get('player', pg.sprite.Group())
        ):
            animation = player.parent.animation
            if (animation and
                player.parent.state == 'damage' and
                animation.active
            ): continue

            damage_direction = diff_vec(
                player.rect.center, self.rect.center
            ).normalize()
            player.signal([
                'damage', 1, damage_direction
            ])
            
