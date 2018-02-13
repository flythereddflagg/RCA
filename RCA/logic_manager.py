# logic_manager.py
from constants import *


class LogicManager():
    
    def __init__(self, eng):
        self.eng         = eng
        self.all_sprites = self.eng.all_sprites
        self.background  = self.eng.background
        
    
    def logic(self):
        self.all_sprites.update()
        self.background.update()
    
    def move(self, pixels, dir):
        self.direction = dir
        self.image = self.consts[dir][1]\
            if self.counter < PLRANIRT / 2 else\
            self.consts[dir][2]
        self.counter += 1
        if self.counter > PLRANIRT: self.counter = 0 # reset counter
        if self.rect.x < CENTERX - CAMERASLACK or\
                self.rect.x > CENTERX + CAMERASLACK or\
                self.rect.y < CENTERY - CAMERASLACK or\
                self.rect.y > CENTERY + CAMERASLACK:
            self.mv_background(pixels)
        else:
            if   dir == N:
                self.rect.y -= pixels
            elif dir == E:
                self.rect.x += pixels
            elif dir == S:
                self.rect.y += pixels
            elif dir == W:
                self.rect.x -= pixels
