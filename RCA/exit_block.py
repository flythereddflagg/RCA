from constants import *
from block import Block

class ExitBlock(Block):
    def __init__(self, 
            image_path,
            xposition, 
            yposition,
            scale = 1,
            rotate = 0):
        
        super().__init__(
                image_path,
                xposition,
                yposition,
                scale,
                rotate)
    
    def blk_do(self):
        return "Zone 2"


def main():
    b = ExitBlock(
        "./sprites/backgrounds/zone1.png",
        1,1)
            
if __name__ == "__main__":
    main()
