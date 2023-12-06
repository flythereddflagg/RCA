import pygame as pg
from .sprite import Character, Decal
from .compass import Compass

DEFAULT_ANIMATION = 'stand'

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO: redo speeds in terms of subpixels so this can scale
        self.PLAYERSPEED = 300 # pixels per second
        self.todo_list = []
        self.dist_per_frame = self.PLAYERSPEED // self.game.FPS
        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}
        self.button1_action = 'sword swing'


    def apply_todos(self):
        
        for action in self.todo_list:
            if self.animation_active: continue

            if action in Compass.strings: 
                # ^ means a direction button is being pressed
                self.move(Compass.vec_map[action], self.dist_per_frame)
                self.direction = Compass.i_map[action]
                self.animate_data = self.animation['walk']
                # self.animation_active = False
                
            elif action == "BUTTON_1":
                self.keys_held[action] = True
                self.animate_data = self.animation[self.button1_action]
                self.animation_active = True

            else:
                print(action + "! (no response)")
                return


    def update(self):
        todo_list_bak = self.todo_list.copy()
        self.todo_list = [
            todo for todo in self.todo_list
            if not self.keys_held[todo]
        ]
        
        self.apply_todos()
        # for action in self.todo_list:
        #     self.apply_todos(action)

        if not self.todo_list and not self.animation_active:
            self.animate_data = self.animation[DEFAULT_ANIMATION]

        self.animate()

        # reset the todo_list
        self.todo_list = []

        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}
        for direction in Compass.strings:
            if direction in todo_list_bak:
                todo_list_bak.remove(direction)
        for todo in todo_list_bak:
            self.keys_held[todo] = True


    def add_todo(self, action):
        self.todo_list.append(action)

