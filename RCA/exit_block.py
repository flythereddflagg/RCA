from constants import *
from block import Block

class ExitBlock(Block):
    def __init__(self, 
            img_path,
            xpos, 
            ypos,
            scale = 1,
            rotate = 0):
        
        super().__init__(
                img_path,
                xpos, 
                ypos,
                scale,
                rotate)
    
    def blk_do(self):
        print("This block did a thing!")


def main():
    b = ExitBlock(
        "./sprites/backgrounds/zone1.png",
        1,1)
            
if __name__ == "__main__":
    main()
