"""
File     : zone1.py
Author   : Mark Redd

First zone in game.

"""
from constants import *
from block import Block
from background import Background

class Zone1():
    def __init__(self, game):
        self.game = game
        background_path = "./sprites/backgrounds/zone1.png"
        self.background = Background(-1500, -1150, background_path)
        self.game.background.add(self.background)
        self.game.all_sprites.add(self.background)
        self.update()
    
    def update(self):
        self.block_list = []
        self.bgx0 = self.background.rect.x
        self.bgy0 = self.background.rect.y
        for sprt in self.game.blocks.sprites():
            sprt.kill()
        with open('zone1.csv', 'r') as f:
            for line in f:
                if line[0] == '#': continue
                row = line.split(',')
                if not(len(row) == 5 or len(row) == 0):
                    raise RCAException(
                        "Invalid in-game configuration file syntax")
                self.block_list.append(
                    # xpos, ypos, path
                    Block(
                        row[0],
                        self.bgx0 + int(row[1]), 
                        self.bgy0 + int(row[2]),
                        int(row[3]),
                        int(row[4])))
        self.game.blocks.add(self.block_list)
        self.game.all_sprites.add(self.block_list)
        
