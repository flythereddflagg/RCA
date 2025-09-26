import math
import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .tools import list_collided, vec, diff_vec
from .item import EMPTY
from .node import Node

# DEFAULT_SPEED = 130
DEFAULT_SPEED = 300

DEFAULT_STATE = 'stand'
LEFT_HAND_BUTTON = "BUTTON_S"
RIGHT_HAND_BUTTON = "BUTTON_E"
RIGHT_STICK_AX = ["R_"+direction for direction in Compass.strings]
LEFT_STICK_AX = ["L_"+direction for direction in Compass.strings]


class Player(Node):

    def setup(self):
        # breakpoint()
        self.move = Movement(self.sprite)
        self.speed = DEFAULT_SPEED
        self.signals = []
        self.input_held = []
        self.damage_direction = vec((0,1))
        self.state = DEFAULT_STATE


    def update(self):
        self.apply_input()
        self.check_signals()
        self.check_collision()
        # self.children.update()
        self.apply_physics()
        
        if self.inventory.hp <= 0:
            self.sprite.kill()


    def signal(self, signal_):
        self.signals.append(signal_)


    def apply_direction(self, actions, values):
        # move in a direction
        dirs = 0
        for direction in Compass.strings:
            if not (direction in actions): continue
            dirs +=1
            self.move(direction, speed=self.speed)
            self.state = 'walk'


    def apply_buttons(self, actions, values):
        if (LEFT_HAND_BUTTON in actions and 
            LEFT_HAND_BUTTON not in self.input_held
        ):
            if self.inventory.left_item.id != EMPTY:
                self.animation_id = self.inventory.left_item.action
                if self.animation_id:
                    self.state = self.animation_id
        
        if (RIGHT_HAND_BUTTON in actions and 
            RIGHT_HAND_BUTTON not in self.input_held
        ):
            if self.inventory.right_item.id != EMPTY:
                self.animation_id = self.inventory.right_item.action
                if self.animation_id:
                    self.state = self.animation_id


    def apply_input(self):
        if self.animation and self.animation.active: 
            return
        actions_val, self.input_held = self.scene.game.input.get()

        # revert to "idle" self.animation if no input is given
        if not actions_val:
            self.state = DEFAULT_STATE
            return

        actions, values = list(map(list, zip(*actions_val)))

        self.apply_direction(actions, values)
        # self.apply_right_stick(actions, values)
        self.apply_buttons(actions, values)


    def apply_physics(self):
        if self.state == 'damage':
            self.move(
                self.damage_direction, 
                speed=3*self.speed, 
                change_direction=False
            )
        # TODO -3- refine how damage works including Iframes, knockback and stuff like that.
        # split damage into knockback and other various states that need to be applied


    def signal(self, signal):
        self.signals.append(signal)


    def check_signals(self):
        for signal in self.signals:
            if "damage" in signal[0]:
                self.inventory.change_health(-signal[1])
                self.damage_direction = signal[2]
                self.state = 'damage'

        self.signals = [] # reset signals


    def check_collision(self):
        if not (self.state == "sword" and "foe" in self.scene.groups):
            return
        hurt_sprites = [
            getattr(sprite, "hurtmask", sprite).sprite
            for sprite in self.scene.groups['foe']
        ]
        for sprite in list_collided(self.hitmask.sprite, hurt_sprites):
            if getattr(sprite, "state", "") == 'damage': continue
            damage_direction = diff_vec(
                 sprite.rect.center, self.sprite.rect.center
            ).normalize()
            sprite.signal([
                "damage", 10, damage_direction
            ])

