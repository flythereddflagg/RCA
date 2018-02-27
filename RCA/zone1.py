# zone1.py
from constants import *
from block import Block

class Zone1():
    def __init__(self, eng):
        self.eng = eng
        self.background = self.eng.bkgnd
        bgx0 = self.background.rect.x
        bgy0 = self.background.rect.y
        background_path = "./sprites/backgrounds/zone1.png"
        
        self.blocks = [
            # xpos, ypos, path
            Block(
                bgx0 + 510 + 60*i, 
                bgy0 + 1620,
                "./sprites/blocks/rock_wall.png")\
            for i in range(10)
            ]
            self.eng.blocks.add(self.blocks)
            self.eng.all_sprites.add(self.blocks)
        
    
    def update(self):
        self.blocks = 
        
        