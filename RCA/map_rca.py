# map_rca.py
from constants import *

class MapRCA():
    def __init__(self, eng = None, bkgnd = None):
        self.eng = eng
        self.background = self.eng.bkgnd
        background_path = "./sprites/backgrounds/zone1.png"
        self.update_from_file()
    
    def get_map_sprites(self):
        pass
    
    def update_from_file(self):
        self.block_list = []
        self.bgx0 = self.background.rect.x
        self.bgy0 = self.background.rect.y
        for sprt in self.eng.block_list.sprites():
            sprt.kill()
        
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
        
        def parse_file(self):
            with open('zone1.conf', 'r') as f:
            for line in f:
                if line[0] == '#': continue
                row = line.split(',')
                if not(len(row) == 5 or len(row) == 0):
                    raise RCAException(
                        "Invalid in-game configuration file syntax")

def main():
    mp = MapRCA()
                        
if __name__ == '__main__':
    main()