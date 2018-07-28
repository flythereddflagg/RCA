from constants import *
from block import Block

class ExitBlock(Block):
    def __init__(self, 
            image_path,
            xposition, 
            yposition,
            scale,
            rotate,
            command):
        
        super().__init__(
                image_path,
                xposition,
                yposition,
                scale,
                rotate)
        self.command = command


