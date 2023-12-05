import pygame as pg
from .sprite import Character, Decal
from .compass import Compass


class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        # TODO: redo speeds in terms of subpixels so this can scale
        self.PLAYERSPEED = 300 # pixels per second
        self.dist_per_frame = self.PLAYERSPEED // self.game.FPS
        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}


    def apply_action(self, action):
        if self.animation_active: return

        if action in Compass.strings: 
            # ^ means a direction button is being pressed
            self.move(Compass.vec_map[action], self.dist_per_frame)
            self.direction = Compass.i_map[action]
            self.animate_data = self.animation['walk']
            
        elif action == "BUTTON_1":
            self.keys_held[action] = True
            self.animation_active = True
            self.animate_data = self.animation['sword swing']
            # TODO: make it so that the action happens only once until you let go of the button.

        else:
            print(action + "! (no response)")
            return

    def update(self):
        todo_list_bak = self.todo_list.copy()
        self.todo_list = [
            todo for todo in self.todo_list
            if not self.keys_held[todo]
        ]
        super().update()
        self.keys_held = {key:False for key in self.game.KEY_BIND.keys()}
        for todo in todo_list_bak:
            self.keys_held[todo] = True

