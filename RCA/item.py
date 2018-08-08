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
        self.img_paths = [
            "./sprites/items/sword.png"
            ]
        self.original_size = (32,32)
        self.size_multiplier = 1.5
        self.size = (
            int(self.original_size[0] * self.size_multiplier),
            int(self.original_size[1] * self.size_multiplier))
        self.images = () 
        self.direction = S
        self.image = self.gen_img("./sprites/items/sword.png")
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.mask = pg.mask.from_surface(self.image)
        
    def gen_img(self, path):
        return pg.transform.scale(
            pg.image.load(path).convert_alpha(), 
            self.size)
    
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


        