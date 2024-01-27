import math
import pygame as pg
from .character import Character
from .compass import Compass

DEFAULT_ANIMATION = 'stand'

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO: redo speeds in terms of subpixels so this can scale
        self.speed = 300 # pixels per second
        self.todo_list = []
        self.signals = []
        # self.dist_per_frame = self.speed // self.scene.clock.get_fps()
        # self.dist_per_frame = math.ceil(self.speed * self.scene.dt / 1000)
        self.keys_held = {key:False for key in self.scene.game.KEY_BIND.keys()}
        self.button1_action = 'sword swing'
        self.hp = 100
        self.damage_direction = pg.math.Vector2(0,1)

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
            if self.animation.active: continue
            # TODO abstract decisions
            if action in Compass.strings:
                # ^ means a direction button is being pressed                
                self.move(action, speed=self.speed)
                self.animation.current = self.animation.data['walk']
                
            elif action == "BUTTON_1":
                self.keys_held[action] = True
                self.animation.current = self.animation.data[
                    self.button1_action]
                self.animation.active = not self.animation.current["repeat"]

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
        self.animation.animate()
        if self.animation.current['id'] == 'damage' and self.animation.active:
                self.move(self.damage_direction, speed=3*self.speed)

    def update(self):
        self.apply_todos()
        self.check_collision()
        self.check_signals()
        self.animate()
        
        if self.hp <= 0:
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
                self.hp -= signal[1]
                self.damage_direction = signal[2]
                self.animation.current = self.animation.data['damage']
                self.animation.active = not self.animation.current["repeat"]
            # TODO abstract this out into sprite

        self.signals = [] # reset signals

    def check_collision(self):
        if self.animation.current['id'] == 'damage' and self.animation.active:
            return
        if self.animation.alt_sprite.mask:
            for sprite in pg.sprite.spritecollide(
                # collide between character and foreground
                self.animation.alt_sprite, self.scene.groups['foe'], 
                # do not kill, use the masks for collision
                False, pg.sprite.collide_mask
            ):
                sprite.signal([
                    "damage", 10, Compass.opposite(self.direction)
                ])

