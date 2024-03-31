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
        # TODO? LOW implement acceleration and momentum
        self.speed = 300
        self.todo_list = []
        self.signals = []
        self.damage_direction = pg.math.Vector2(0,1)
        self.move = Movement(self, **self.options)
        self.animation = Animation(self, **self.options)
        self.inventory = Inventory(self, money=0, hp=100, hp_max=100)


    def apply(self, game_input):
        self.todo_list.extend(game_input)


    def apply_todos(self):
        input_held = self.scene.game.input.input_held
        # todo_list_bak = self.todo_list.copy()
        # self.todo_list = [
        #     todo for todo in self.todo_list
        #     if not self.keys_held[todo]
        # ]
        # revert to "idle" animation if no input is given
        if not self.todo_list and not self.animation.active:
            self.animation.current = self.animation.data[DEFAULT_ANIMATION]

        vector = pg.math.Vector2([0,0])
        for action in self.todo_list:
            if isinstance(action, tuple):
                action, value = action
            else:
                action, value = action, 0.0
            # TODO make a complete action list and implement
            if self.animation.active: continue
            if action in Compass.strings:
                # ^ means a direction button is being pressed                
                self.move(action, speed=self.speed * self.scale)
                self.animation.current = self.animation.data['walk']
                
            elif action == "BUTTON_1":
                if self.inventory.active:
                    if input_held[action]: continue
                    self.inventory.select('LEFT')
                    continue
                if self.inventory.left_item is None: continue
                self.animation.current = self.animation.data[
                    self.inventory.left_item.select()
                ]
            elif action == "BUTTON_2":
                if self.inventory.active:
                    if input_held[action]: continue
                    self.inventory.select('RIGHT')
                    continue
                if self.inventory.right_item is None: continue
                self.animation.current = self.animation.data[
                    self.inventory.right_item.select()
                ]

            # elif input_held["BUTTON_3"] and not self.inventory.active:
                
        
            elif action in ["R_UP","R_DOWN","R_LEFT","R_RIGHT"]:
                if not self.inventory.active:
                    self.inventory.active = True
                    self.inventory.toggle()
                multiplier = abs(value) if value else 1.0
                    
                vector += (
                    Compass.vector(action[2:]) * 
                    self.inventory.image.get_height() * 
                    multiplier
                )

            else:
                print(str(action) + "! (no response)")
            
            if vector.magnitude():
                self.inventory.marker.rect.center = (
                    self.inventory.rect.center + 
                    vector
                )
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

