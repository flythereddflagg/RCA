from constants import *
from block import Block

class ExitBlock(Block):
    def __init__(self, 
            image_path,
            xposition, 
            yposition,
            scale,
            rotate,
            go_to,
            coord,
            direction,
            playerx,
            playery):
        
        super().__init__(
                image_path,
                xposition,
                yposition,
                scale,
                rotate)
        self.go_to = go_to
        self.coord = coord
        self.direction = direction
        self.playerx = playerx
        self.playery = playery

        

