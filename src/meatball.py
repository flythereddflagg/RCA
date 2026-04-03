import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node
from .tools import vec, mask_collision, diff_vec

DIST_SQR_AGRO = 100**2

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        self.move = Movement(self.sprite, hitmask_sprite = self.hitmask.sprite)
        self.state = "stage1"
        self.animation.set_state(self.state)
        self.cur_action = 4
        self.hp = 20
        self.signals = []
    

    def signal(self, signal_):
        self.signals.append(signal_)

    
    def check_signals(self):
        for name, value, other in self.signals:
            if "damage" in name and self.state != "damage":
                self.hp -= value
                self.damage_direction = other
                self.state = 'damage'

        self.signals = [] # reset signals


    def update(self):
        player = self.scene.get_player().parent
        if player.inventory.contains("sword"):
            self.stage3()
            return
        elif player.inventory.contains("shovel"):
            self.state = "stage2"
            self.animation.set_state(self.state)
        self.random_movement()

        
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

    def stage3(self):
        self.check_signals()
        player_sprite = self.scene.get_player()
        if (
            vec(self.sprite.rect.center).distance_squared_to(
                player_sprite.rect.center
            ) < DIST_SQR_AGRO
        ):
            self.animation.set_state("throw")
        
        else:
            self.animation.set_state("wiggle")

        if mask_collision(self.hitmask.sprite, player_sprite):
            damage_direction = diff_vec(
                player_sprite.rect.center, self.hitmask.sprite.mask.centroid()
            ).normalize()
            player_sprite.signal(['damage', 1, damage_direction])
        
        if self.hp <= 0:
            self.kill()

