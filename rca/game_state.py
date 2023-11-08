import pygame as pg

from .sprite import Player
from .dict_obj import DictObj

class GameState(DictObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.groups = []
        self.running = False
        self.SCREENSIZE = (self.SCREENWIDTH, self.SCREENHEIGHT)
        # x and y coordinates for the center of the screen
        self.CENTERX = self.SCREENWIDTH  // 2 
        self.CENTERY = self.SCREENHEIGHT // 2
        # TODO organize groups
        # TODO load game from YAML
        
        self.player = Player()
        self.player.rect.x = self.CENTERX
        self.player.rect.y = self.CENTERY
        self.groups.append(pg.sprite.Group())
        self.groups[-1].add(self.player)
    
    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
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
