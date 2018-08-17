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
        self.scale = 3

        paths = [
            "./sprites/player_sprite/larry_wk1_S.png",
            "./sprites/items/sword_swing/Larry_swing_S1.png",
            "./sprites/items/sword_swing/Larry_swing_S2.png",
            "./sprites/items/sword_swing/Larry_swing_S3.png",
            ]
        
        self.images = (
            (self.gen_img(paths[0]), 0,0),
            (self.gen_img(paths[0]), 0,0),
            (self.gen_img(paths[1]), -54,-36),
            (self.gen_img(paths[2]), -54,-36),
            (self.gen_img(paths[3]), -54,-36),
            )
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pg.mask.from_surface(self.image)
        self.counter = 1
        self.frame_counter = 0
        self.animate_frames = 0

            
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
        
        
    def gen_img(self, path):
        image = pg.image.load(path).convert_alpha()
        width, height = image.get_size()
        width *= self.scale
        height *= self.scale
        return pg.transform.scale(
                    image,
                    (int(width), int(height))) 
        