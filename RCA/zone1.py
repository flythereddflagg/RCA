# zone1.py
from constants import *
from block import Block

class Zone1():
    def __init__(self, eng):
        self.eng = eng
        background_pos_ini = (-200,-1200)
        bgx0 = background_pos_ini[0]
        bgy0 = background_pos_ini[1]
        background_path = "./sprites/backgrounds/zone1.png"
        
        blocks = [
            # xpos, ypos, path
            Block(510 + 60*i,1620,"./sprites/blocks/rock_wall.png")\
            for i in range(10)
            ]
