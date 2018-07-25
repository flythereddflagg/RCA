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

    def update(self):
        self.groups = [[], []]
        self.bgx0 = self.background.rect.x
        self.bgy0 = self.background.rect.y
        for sprite in self.game.blocks.sprites():
            sprite.kill()
        with open('zone1.csv', 'r') as f:
            for line in f:
                if line[0] == '#': continue
                row = line.split(',')
                if not(len(row) == 6 or len(row) == 0):
                    raise RCAException(
                        "Invalid in-game configuration file syntax")
                btype = int(row[5])
                if btype == 0:
                    blk = Block(
                            row[0],
                            self.bgx0 + int(row[1]), 
                            self.bgy0 + int(row[2]),
                            int(row[3]),
                            int(row[4]))
                elif btype == 1:
                    blk = ExitBlock(
                            row[0],
                            self.bgx0 + int(row[1]), 
                            self.bgy0 + int(row[2]),
                            int(row[3]),
                            int(row[4]))
                else:
                    raise RCAException(
                        "ConfError: Class does not exist!")
                self.groups[int(row[5])].append(blk)
                    
        
        self.game.blocks.add(self.groups[0])
        self.game.hblocks.add(self.groups[1])
        self.game.all_sprites.add(self.groups[0])
        self.game.all_sprites.add(self.groups[1])
        
        
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
            
