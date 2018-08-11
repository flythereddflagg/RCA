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
        self.size_multiplier = 1.5
        
        self.image = pg.image.load(path).convert_alpha()
        width, height = self.image.get_size()
        width *= scale
        height *= scale
        self.image = pg.transform.scale(
                    self.image,
                    (int(width), int(height))) 
        self.image = self.base_image
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pg.mask.from_surface(self.image)
        
    
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


        