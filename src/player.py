import math
import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
# from .animations import animations
# from .inventory import Inventory
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
# TODO implement the left stick with the above line


class Player(Node):
    def __init__(self, **init):
        super().__init__(**init)
        self.init = init
        self.speed = DEFAULT_SPEED
        self.todo_list = []
        self.signals = []
        self.sprite = Decal(parent=self, **init)
        
        self.damage_direction = pg.math.Vector2(0,1)
        self.move = Movement(self.sprite, **self.init)
        ## TEMP work around
        # opts = self.animations.
        # self.hitmask = HitMask(
        #     self, opts['animations'], opts["path_prefix"]
        # )
        self.input_held = None
        self.state = DEFAULT_STATE

    def signal(self, signal_):
        self.signals.append(signal_)


    def apply(self, game_input):
        self.todo_list.extend(game_input)

    def get_actions_values(self):
        actions, values = [], []
        for action in self.todo_list:
            if isinstance(action, tuple):
                action, value = action
            elif isinstance(action, str):
                action, value = action, 0.0
            else:
                raise ValueError(f"Invalid input: {action}")

            actions.append(action)
            values.append(value)
        return actions, values


    def apply_direction(self, actions, values):
        # move in a direction
        dirs = 0
        for direction in Compass.strings:
            if not (direction in actions): continue
            dirs +=1
            self.move(direction, speed=self.speed * self.sprite.scale)
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
            not self.input_held[LEFT_HAND_BUTTON]
        ):
            if self.inventory.active:
                self.inventory.select("LEFT")
            elif self.inventory.left_item.id != EMPTY:
                self.animations_id = self.inventory.left_item.action
                if self.animations_id:
                    self.state = self.animations_id
        
        if (RIGHT_HAND_BUTTON in actions and 
            not self.input_held[RIGHT_HAND_BUTTON]
        ):
            if self.inventory.active:
                self.inventory.select("RIGHT")
            elif self.inventory.right_item.id != EMPTY:
                self.animations_id = self.inventory.right_item.action
                if self.animations_id:
                    self.state = self.animations_id


    def apply_input(self):
        if self.animations and self.animations.active: 
            # reject all current todos
            self.todo_list = [] 
            return
        self.todo_list.extend(self.scene.game.input.get())
        self.input_held = self.scene.game.input.held

        # revert to "idle" self.animations if no input is given
        if (
            not self.todo_list and 
            (not self.animations or not self.animations.active)
        ):
            self.state = DEFAULT_STATE
            return

        actions, values = self.get_actions_values()

        self.apply_direction(actions, values)
        self.apply_right_stick(actions, values)
        self.apply_buttons(actions, values)

        # reset the todo_list
        self.todo_list = [] 


    def apply_physics(self):
        if self.state == 'damage':
            self.move(
                self.damage_direction, 
                speed=3*self.speed, 
                change_direction=False
            )
        # TODO refine how damage works including Iframes, knockback and stuff like that.
        # split damage into knockback and other various states that need to be applied
        



    def update(self):
        # print(
        #     "player pos", 
        #     self.sprite.rect.topleft, 
        #     pg.math.Vector2(self.sprite.rect.topleft) - 
        #     pg.math.Vector2(self.scene.background.sprites()[0].rect.topleft)
        # )
        self.apply_input()
        self.check_signals()
        self.check_collision()
        self.children.update()
        # self.self.animations.update()
        # self.hitmask.update()
        self.inventory.update()
        self.apply_physics()
        
        if self.inventory.hp <= 0:
            self.sprite.kill()
        # print(self.sprite.rect.topleft)


    def add_todo(self, action):
        self.todo_list.append(action)


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

