from constants import *
from block import Block

class ExitBlock(Block):
    def __init__(self, 
            image_path,
            xposition, 
            yposition,
            scale,
            rotate):
        
        super().__init__(
                image_path,
                xposition,
                yposition,
                scale,
                rotate)
        self.command = "zone2.json"


def main():
    b = ExitBlock(
        "./sprites/backgrounds/zone1.png",
        1,1)
            
if __name__ == "__main__":
    main()
