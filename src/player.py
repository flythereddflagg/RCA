import math
import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .tools import list_collided
from .item import EMPTY
from .node import Node
from .hit_mask import HitMask

DEFAULT_SPEED = 200
DEFAULT_STATE = 'stand'
LEFT_HAND_BUTTON = "BUTTON_1"
RIGHT_HAND_BUTTON = "BUTTON_2"
RIGHT_STICK_AX = ["R_"+direction for direction in Compass.strings]
LEFT_STICK_AX = ["L_"+direction for direction in Compass.strings]


class Player(Node):
    def __init__(self, **init):
        super().__init__(**init)
        self.init = init
        self.speed = DEFAULT_SPEED
        self.signals = []
        self.input_held = []
        self.sprite = Decal(parent=self, **init)
        self.damage_direction = pg.math.Vector2(0,1)
        self.move = Movement(self.sprite, **self.init)
        self.state = DEFAULT_STATE


    def update(self):
        self.apply_input()
        self.check_signals()
        self.check_collision()
        self.children.update()
        self.inventory.update()
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


    def apply_right_stick(self, actions, values):
        # activate inventory
        vector = pg.math.Vector2([0,0])
        for direction in RIGHT_STICK_AX:
            if not (direction in actions): continue
            value = values[actions.index(direction)]
            if not self.inventory.active: self.inventory.toggle()
            multiplier = abs(value) if value else 1.0
            vector += (
                Compass.vector(direction[2:]) * 
                self.inventory.sprite.image.get_height() * 
                multiplier
            )

        self.inventory.marker.rect.center = (
            self.inventory.sprite.rect.center + 
            vector
        )


    def apply_buttons(self, actions, values):
        if (LEFT_HAND_BUTTON in actions and 
            LEFT_HAND_BUTTON not in self.input_held
        ):
            if self.inventory.active:
                self.inventory.select("LEFT")
            elif self.inventory.left_item.id != EMPTY:
                self.animations_id = self.inventory.left_item.action
                if self.animations_id:
                    self.state = self.animations_id
        
        if (RIGHT_HAND_BUTTON in actions and 
            RIGHT_HAND_BUTTON in self.input_held
        ):
            if self.inventory.active:
                self.inventory.select("RIGHT")
            elif self.inventory.right_item.id != EMPTY:
                self.animations_id = self.inventory.right_item.action
                if self.animations_id:
                    self.state = self.animations_id


    def apply_input(self):
        if self.animations and self.animations.active: 
            return
        actions_val, self.input_held = self.scene.game.input.get()

        # revert to "idle" self.animations if no input is given
        if not actions_val:
            self.state = DEFAULT_STATE
            return

        actions, values = list(map(list, zip(*actions_val)))
        print("a", actions, "v", values)

        self.apply_direction(actions, values)
        self.apply_right_stick(actions, values)
        self.apply_buttons(actions, values)


    def apply_physics(self):
        if self.state == 'damage':
            self.move(
                self.damage_direction, 
                speed=3*self.speed, 
                change_direction=False
            )
        # TODO refine how damage works including Iframes, knockback and stuff like that.
        # split damage into knockback and other various states that need to be applied


    def signal(self, signal):
        self.signals.append(signal)


    def check_signals(self):
        if self.signals: print(f"[{self.id}] got signals:{self.signals}")
        for signal in self.signals:
            if "damage" in signal[0]:
                self.inventory.change_health(-signal[1])
                self.damage_direction = signal[2]
                self.state = 'damage'

        self.signals = [] # reset signals


    def check_collision(self):
        if self.state == "sword":
            for sprite in list_collided(
                self.hitmask.sprite, self.scene.groups['foe']
            ):
                if sprite.state == 'damage': continue
                damage_direction = (
                    pg.math.Vector2(sprite.rect.center) -
                    pg.math.Vector2(self.sprite.rect.center)
                ).normalize()
                sprite.signal([
                    "damage", 10, damage_direction
                ])

