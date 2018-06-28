# map_rca.py
from constants import *
from pprint import pprint

class MapRCA():
    def __init__(self, eng = None, bkgnd = None):
        self.eng = eng
        self.background = None if self.eng == None else self.eng.bkgnd
        self.conf = {}
        background_path = "./sprites/backgrounds/zone1.png"
        #self.update_from_file()
    
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
            lines = f.readlines()
        pprint(lines)
        for line in lines:
            if line[0] == '#' or\
                line.isspace(): 
                continue
            if '=' in line:
                row = line.split(' = ')
                if len(row) != 2:
                    raise RCAException(
                        "Invalid in-game configuration file syntax")
                if '{' in row[1]:
                    key1 = row[0]
                    self.conf = 
            row = line.split(',')
            if not(len(row) == 5 or len(row) == 0):
                raise RCAException(
                    "Invalid in-game configuration file syntax")

def main():
    mp = MapRCA()
    mp.parse_file()
                        
if __name__ == '__main__':
    main()