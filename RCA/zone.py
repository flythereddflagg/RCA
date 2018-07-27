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

class Zone():
    def __init__(self, game, config_path):
        self.game = game
        self.config_path = config_path
        self.background = None
        self.background_x = None
        self.background_y = None
        self.update()
    
    def update(self):
        if self.background:
            self.background_x = self.background.rect.x
            self.background_y = self.background.rect.y
        for sprite_group in self.game.diegetic_groups:
            for sprite in sprite_group:
                sprite.kill()
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        self.background = Background(**config['background'])
        self.game.background.add(self.background)
        self.game.all_sprites.add(self.background)
        
        if self.background_x == None or self.background_y == None:
            self.background_x = self.background.rect.x
            self.background_y = self.background.rect.y
        else:
            self.background.rect.x = self.background_x
            self.background.rect.y = self.background_y 
        
        self.foreground = Block(**config['foreground'])
        self.foreground.rect.x += self.background_x
        self.foreground.rect.y += self.background_y
        self.game.foreground.add(self.foreground)
        self.game.all_sprites.add(self.foreground)
        
        for exit_block_conf in config['exit_blocks']:
            blk = ExitBlock(**exit_block_conf)
            blk.rect.x += self.background_x
            blk.rect.y += self.background_y
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
    
    def blk_do(self, block_instance):
        zone_path = block_instance.command
        self.game.cur_zone = Zone(self.game, zone_path)
