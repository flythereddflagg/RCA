import math
import pygame as pg
from .sprite import Character
from .compass import Compass

DEFAULT_ANIMATION = 'stand'

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO: redo speeds in terms of subpixels so this can scale
        self.speed = 300 # pixels per second
        self.todo_list = []
        self.signals = []
        # self.dist_per_frame = self.speed // self.game.clock.get_fps()
        # self.dist_per_frame = math.ceil(self.speed * self.game.dt / 1000)
        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}
        self.button1_action = 'sword swing'
        # TODO add hit mask here


    def apply_todos(self):
        todo_list_bak = self.todo_list.copy()
        self.todo_list = [
            todo for todo in self.todo_list
            if not self.keys_held[todo]
        ]
        if not self.todo_list and not self.animation_active:
            self.animate_data = self.animation[DEFAULT_ANIMATION]

        for action in self.todo_list:
            if self.animation_active: continue

            if action in Compass.strings:
                fps = self.game.clock.get_fps()
                if not fps: continue
                # ^ means a direction button is being pressed
                self.move(Compass.vec_map[action], 
                    self.speed / fps
                )
                self.direction = Compass.i_map[action]
                self.animate_data = self.animation['walk']
                
            elif action == "BUTTON_1":
                self.keys_held[action] = True
                self.animate_data = self.animation[self.button1_action]
                self.animation_active = not self.animate_data["repeat"]

            else:
                print(action + "! (no response)")

        # reset the todo_list
        self.todo_list = []
        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}
        for direction in Compass.strings:
            if direction in todo_list_bak:
                todo_list_bak.remove(direction)
        for todo in todo_list_bak:
            self.keys_held[todo] = True

    
    def update(self):
        self.check_signals()
        self.apply_todos()
        self.animate()


    def add_todo(self, action):
        self.todo_list.append(action)

    def signal(self, signal):
        self.signals.append(signal)

    def check_signals(self):
        self.signals = [] # reset signals
    # TODO implement this so it checks stuff from other sprites

