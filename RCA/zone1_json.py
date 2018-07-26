"""
File     : zone1.py
Author   : Mark Redd

First zone in game.

"""
import json
from constants import *
from block import Block
from exit_block import ExitBlock
from background import Background

class Zone1():
    def __init__(self, game):
        self.game = game
        
        with open("zone1.json", 'r') as f:
            config = json.load(f)
        
        self.background = Background(**config['background'])
        self.game.background.add(self.background)
        self.game.all_sprites.add(self.background)
        
        self.foreground = Block(**config['foreground'])
        self.game.foreground.add(self.foreground)
        self.game.all_sprites.add(self.foreground)
        
        for exit_block_conf in config['exit_blocks']:
            blk = ExitBlock(**exit_block_conf)
            self.game.blocks.add(blk)
            self.game.all_sprites.add(blk)
        
    def edge(self, direction):
        """
        Returns True if the @param 'direction' edge of the zone is visble 
        inside the frame. Else returns False.
        """
        edge_bools = [
            self.background.rect.y > -PLAYERSPEED,
            self.background.rect.x < (
                SCREENWIDTH - self.background.width + PLAYERSPEED),
            self.background.rect.y < (
                SCREENHEIGHT - self.background.height + PLAYERSPEED),
            self.background.rect.x > -PLAYERSPEED]
        return edge_bools[direction]
            
