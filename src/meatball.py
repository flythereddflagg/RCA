import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node
from .tools import vec, mask_collision, diff_vec
from .compass import Compass

DIST_SQR_AGRO = 100**2
BASE_SPEED = 25

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        self.move = Movement(self.sprite, hitmask_sprite = self.hitmask.sprite)
        self.animation.set_state("stage1")
        self.cur_action = 4
        self.hp = 30
        self.signals = []
        self.agro = False
        self.stage3_go = False
    

    def signal(self, signal_):
        self.signals.append(signal_)

    
    def check_signals(self):
        for name, value, other in self.signals:
            if "damage" in name and self.animation.state != "damage":
                self.hp -= value
                self.damage_direction = other
                self.animation.set_state("damage")
                print(f"Meatball took damage {value}")
                # TODO -1- get damage direction to act like it

        self.signals = [] # reset signals


    def update(self):
        print(self.animation.state)
        if self.stage3_go:
            self.stage3()
            return
        player = self.scene.get_player().parent
        if player.inventory.contains("sword"):
            if self.animation.state == "stage1":
                self.animation.set_state("stage2")
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
                and self.animation.state == "stage2"
            ):
                self.animation.set_state("transition")
            elif self.animation.state == "wiggle":
                self.stage3_go = True
            return
        elif player.inventory.contains("shovel"): 
            self.animation.set_state("stage2")
        self.random_movement()

        
    def random_movement(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) > 1000:
            self.last_time = cur_time
            self.cur_action = random.randint(0, 4)
        
        if self.cur_action == 4:
            return
        else:
            self.move(self.cur_action, speed=BASE_SPEED)
            # self.move(self.cur_action+random.choice([-1,1]), speed=BASE_SPEED)
            self.move(self.cur_action+1, speed=BASE_SPEED)
            # self.move(3, speed=BASE_SPEED)

    def stage3(self):
        self.check_signals()
        player_sprite = self.scene.get_player()
        if (
            self.animation.state == "wiggle" and 
            vec(self.sprite.rect.center).distance_squared_to(
                player_sprite.rect.center
            ) < DIST_SQR_AGRO
        ):
            self.animation.set_state("throw")
            self.agro = True
        


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
        
        self.apply_physics()



    def chase_player(self):
        player_sprite = self.scene.get_player()
        to_move = diff_vec(
            player_sprite.rect.center, 
            vec(self.hitmask.sprite.mask.centroid())
            + vec(self.sprite.rect.topleft)
            # self.sprite.rect.center
        )
        self.move(Compass.unit_vector(to_move), speed=35)


    def apply_physics(self):
        if self.animation.state == 'damage':
            self.move(
                self.damage_direction, 
                speed=2*BASE_SPEED, 
                change_direction=False
            )