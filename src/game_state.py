import pygame as pg

import src.sprite as sprites
from .dict_obj import DictObj

class GameState(DictObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.running = False
        self.SCREENSIZE = (self.SCREENWIDTH, self.SCREENHEIGHT)
        # x and y coordinates for the center of the screen
        self.CENTERX = self.SCREENWIDTH  // 2 
        self.CENTERY = self.SCREENHEIGHT // 2
        # TODO load game from YAML
        self.groups = [
            pg.sprite.Group() 
            for i in range(len(self.SPRITE_GROUPS))
        ]
    
    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
            print("QUIT!")
            self.running = False
            return

        # apply all the input
        for action in game_input:
            self.apply_action(action)
        
        # update everything else
        for group in self.groups:
            group.update()

    
    def apply_action(self, action):
        print(action + "!")
