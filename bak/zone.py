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
    def __init__(self, game, config_name, background_x=None, background_y=None):
        self.game = game
        self.config_path = DATAPATH.format(config_name)
        self.background = None
        self.background_x = background_x
        self.background_y = background_y
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
        
        try:
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
        except KeyError:
            pass
    
      
    def edge(self, direction):
        """
        Returns True if the @param 'direction' edge of the zone is visible 
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
        if isinstance(block_instance, ExitBlock):
            self.exit_block_do(block_instance)
        
        
    def exit_block_do(self, block_instance):
        zone_path = block_instance.go_to
        if zone_path == '': return
        go_direction = DIRECTION_DICT[block_instance.direction]
        self.game.current_zone = Zone(self.game, zone_path,
            background_x = CENTERX - block_instance.coord[0],
            background_y = CENTERY - block_instance.coord[1])
        self.game.player.rect.x = block_instance.playerx
        self.game.player.rect.y = block_instance.playery

