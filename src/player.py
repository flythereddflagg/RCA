import math
import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .animation import Animation
from .inventory import Inventory
from .tools import list_collided
from .item import EMPTY

DEFAULT_ANIMATION = 'stand'
LEFT_HAND_BUTTON = "BUTTON_1"
RIGHT_HAND_BUTTON = "BUTTON_2"
RIGHT_STICK_AX = ["R_"+direction for direction in Compass.strings]


class Player(Decal):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO? LOW implement acceleration and momentum
        self.speed = 300
        self.todo_list = []
        self.signals = []
        self.damage_direction = pg.math.Vector2(0,1)
        self.move = Movement(self, **self.options)
        self.animation = Animation(self, **self.options)
        self.inventory = Inventory(self, money=0, hp=100, hp_max=100)
        self.input_held = None


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


    def apply_left_stick(self, actions, values):
        # move in a direction
        for direction in Compass.strings:
            if not (direction in actions): continue
            self.move(direction, speed=self.speed * self.scale)
            self.animation.current = self.animation.data['walk']


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
                self.inventory.image.get_height() * 
                multiplier
            )
        if vector.magnitude():
            self.inventory.marker.rect.center = (
                self.inventory.rect.center + 
                vector
            )


    def apply_buttons(self, actions, values):
        # TODO NEXT make it so that non-repeated actions are not repeated with a button held down.
        if LEFT_HAND_BUTTON in actions:
            if self.inventory.active and not self.input_held[LEFT_HAND_BUTTON]:
                self.inventory.select("LEFT")
            elif self.inventory.left_item.id != EMPTY:
                animation_id = self.inventory.left_item.action
                self.animation.current = self.animation.data[animation_id]
        
        if RIGHT_HAND_BUTTON in actions:
            if self.inventory.active and not self.input_held[RIGHT_HAND_BUTTON]:
                self.inventory.select("RIGHT")
            elif self.inventory.right_item.id != EMPTY:
                animation_id = self.inventory.right_item.action
                self.animation.current = self.animation.data[animation_id]


    def apply_todos(self):
        if self.animation.active: 
            # reject all current todos
            self.todo_list = [] 
            return
        self.input_held = self.scene.game.input.held

        # revert to "idle" animation if no input is given
        if not self.todo_list and not self.animation.active:
            self.animation.current = self.animation.data[DEFAULT_ANIMATION]
            return

        actions, values = self.get_actions_values()

        self.apply_left_stick(actions, values)
        self.apply_right_stick(actions, values)
        self.apply_buttons(actions, values)

        # reset the todo_list
        self.todo_list = [] 


    def animate(self):
        self.animation.update()
        if self.animation.current['id'] == 'damage' and self.animation.active:
                self.move(self.damage_direction, speed=3*self.speed)


    def update(self):
        self.apply_todos()
        self.check_collision()
        self.check_signals()
        self.animate()
        self.inventory.update()
        
        if self.inventory.hp <= 0:
            self.scene.player = None
            self.kill()


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
                self.animation.current = self.animation.data['damage']

        self.signals = [] # reset signals


    def check_collision(self):
        if self.animation.current['id'] == 'damage' and self.animation.active:
            return
        if self.animation.alt_sprite.mask:
            for sprite in list_collided(
                self.animation.alt_sprite, self.scene.groups['foe']
            ):
                if (sprite.animation and\
                    sprite.animation.current['id'] == 'damage' and\
                    sprite.animation.active
                ): continue
                damage_direction = (
                    pg.math.Vector2(sprite.rect.center) -
                    pg.math.Vector2(self.rect.center)
                ).normalize()
                sprite.signal([
                    "damage", 10, damage_direction
                ])

