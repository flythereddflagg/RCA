# zone1.py
from constants import *
from block import Block
import csv

class Zone1():
    def __init__(self, eng):
        self.eng = eng
        self.background = self.eng.bkgnd
        background_path = "./sprites/backgrounds/zone1.png"
        self.update()
    
    def update(self):
        self.blocks = []
        self.bgx0 = self.background.rect.x
        self.bgy0 = self.background.rect.y
        for sprt in self.eng.blocks.sprites():
            sprt.kill()
        with open('zone1.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.blocks.append(
                    # xpos, ypos, path
                    Block(
                        row[0],
                        self.bgx0 + int(row[1]), 
                        self.bgy0 + int(row[2]),
                        row[3],
                        row[4]))
        self.eng.blocks.add(self.blocks)
        self.eng.all_sprites.add(self.blocks)
        
        