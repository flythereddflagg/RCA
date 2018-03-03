# zone1.py
from constants import *
from block import Block

class Zone1():
    def __init__(self, eng):
        self.eng = eng
        self.background = self.eng.bkgnd
        background_path = "./sprites/backgrounds/zone1.png"
        self.update()
    
    def update(self):
        self.block_list = []
        self.bgx0 = self.background.rect.x
        self.bgy0 = self.background.rect.y
        for sprt in self.eng.block_list.sprites():
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
        self.eng.block_list.add(self.block_list)
        self.eng.all_sprites.add(self.block_list)
        
        