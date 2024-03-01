import math
import pygame as pg
from .decal import Decal
from .compass import Compass
from .movement import Movement
from .animation import Animation
from .inventory import Inventory
from .tools import list_collided

DEFAULT_ANIMATION = 'stand'

class Player(Decal):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO LOW implement acceleration and momentum
        # self.speed = 150 # pixels per second at original size
        self.speed = 300
        self.todo_list = []
        self.signals = []
        self.keys_held = {key:False for key in self.scene.game.KEY_BIND.keys()}
        self.button1_action = 'sword swing'
        self.damage_direction = pg.math.Vector2(0,1)
        self.move = Movement(self, **self.options)
        self.animation = Animation(self, **self.options)
        self.inventory = Inventory(self.scene, money=0, hp=100, hp_max=100)


    def apply(self, game_input):
        self.todo_list.extend(game_input)


    def apply_todos(self):
        todo_list_bak = self.todo_list.copy()
        self.todo_list = [
            todo for todo in self.todo_list
            if not self.keys_held[todo]
        ]
        if not self.todo_list and not self.animation.active:
            self.animation.current = self.animation.data[DEFAULT_ANIMATION]

        for action in self.todo_list:
            # TODO make a complete action list and implement
            if self.animation.active: continue
            if action in Compass.strings:
                # ^ means a direction button is being pressed                
                self.move(action, speed=self.speed * self.scale)
                self.animation.current = self.animation.data['walk']
                
            elif action == "BUTTON_1":
                self.keys_held[action] = True
                self.animation.current = self.animation.data[
                    self.button1_action]

            elif action == "BUTTON_3":
                self.keys_held[action] = True

            else:
                print(action + "! (no response)")

        # reset the todo_list
        self.todo_list = []
        self.keys_held = {key:False for key in self.scene.game.KEY_BIND.keys()}
        for direction in Compass.strings:
            if direction in todo_list_bak:
                todo_list_bak.remove(direction)
        for todo in todo_list_bak:
            self.keys_held[todo] = True


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

