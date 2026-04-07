import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node
from .tools import vec, mask_collision, diff_vec
from .compass import Compass

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
        self.agro = False
        self.stage3_go = False
    

    def signal(self, signal_):
        self.signals.append(signal_)

    
    def check_signals(self):
        for name, value, other in self.signals:
            if "damage" in name and self.state != "damage":
                self.hp -= value
                self.damage_direction = other
                self.state = 'damage'
                print(f"Meatball took damage {value}")
                # TODO -1- damage animation made

        self.signals = [] # reset signals


    def update(self):
        if self.stage3_go:
            self.stage3()
            return
        player = self.scene.get_player().parent
        if player.inventory.contains("sword"):
            if self.animation.state == "stage1":
                self.state = "stage2"
                self.animation.set_state(self.state)
            self.blockage.kill()
            self.scene.place_node(
                self.blockage, 
                start=(
                    vec(self.blockage.init['start'])
                    + vec(self.scene.background.sprites()[0].rect.topleft)
                ),
                groups=["foreground"]
            )
            if (
                vec(self.sprite.rect.center).distance_squared_to(
                    player.sprite.rect.center
                ) < DIST_SQR_AGRO
                and self.state == "stage2"
            ):
                self.state = "transition"
                self.animation.set_state(self.state)
            elif self.animation.state == "wiggle":
                self.stage3_go = True
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
            self.agro = True
        
        else:
            self.animation.set_state("wiggle")

        if mask_collision(self.hitmask.sprite, player_sprite):
            damage_direction = diff_vec(
                player_sprite.rect.center, 
                vec(self.hitmask.sprite.mask.centroid())
                + vec(self.sprite.rect.topleft)
            ).normalize()
            player_sprite.signal(['damage', 1, damage_direction])
        
        if self.agro and self.animation.state == "wiggle":
            self.chase_player()

        if self.hp <= 0:
            self.kill()


    def chase_player(self):
        player_sprite = self.scene.get_player()
        to_move = diff_vec(
            player_sprite.rect.center, 
            vec(self.hitmask.sprite.mask.centroid())
            + vec(self.sprite.rect.topleft)
            # self.sprite.rect.center
        )
        self.move(Compass.unit_vector(to_move), speed=35)
