"""
File     : item.py
Author   : Mark Redd

item class. Should define all logic relating to the item.
"""
from constants import *
from rca_sprite import SpriteRCA

class Item(SpriteRCA):
    
    def __init__(self, path, player):
        super().__init__()
        self.original_size = (32,32)
        scale = 1.5
        
        self.image = pg.image.load(path).convert_alpha()
        width, height = self.image.get_size()
        width *= scale
        height *= scale
        self.base_image = pg.transform.scale(
                    self.image,
                    (int(width), int(height))) 
        
        self.images = (
            (pg.transform.rotate(self.base_image,  45.0),  -10,-10),
            (pg.transform.rotate(self.base_image,  90.0),  -20,10),
            (pg.transform.rotate(self.base_image,  135.0), -30,20),
            (pg.transform.rotate(self.base_image,  180.0), -10,40),
            )
        self.image = self.images[2][0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pg.mask.from_surface(self.image)
        self.counter = 0
        self.frame_counter = 0
        self.animate_frames = 1
        
    
    def move(self, pixels, dr=None):
        if dr == None: dr = self.direction
        if   dr == N:
            self.rect.y -= pixels
        elif dr == E:
            self.rect.x += pixels
        elif dr == S:
            self.rect.y += pixels
        elif dr == W:
            self.rect.x -= pixels

            
    def use_animate(self, direction=None):
        if self.counter > len(self.images) - 1: self.counter = 0 # reset
        
        self.image = self.images[self.counter][0]
        self.rect.x += self.images[self.counter][1]
        self.rect.y += self.images[self.counter][2]
        
        if self.frame_counter < self.animate_frames:
            self.frame_counter += 1
        else:
            self.frame_counter = 0
            self.counter += 1
        
        
        

        