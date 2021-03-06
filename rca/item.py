"""
File     : item.py
Author   : Mark Redd

item class. Should define all logic relating to the item.
"""
from constants import *
from rca_sprite import SpriteRCA
import json

class Item(SpriteRCA):
    
    def __init__(self, path, player):
        super().__init__()
        self.scale = 3
        self.player = player
        
        with open('./data/item_sword.json', 'r') as f:
            data = json.load(f)
            paths = data["item paths"]
        
        self.images = {
            S:(
                (self.gen_img(paths[0]), 0,0),
                (self.gen_img(paths[1]), -54,-36),
                (self.gen_img(paths[2]), -54,-36),
                (self.gen_img(paths[3]), -54,-36),
                (self.gen_img(paths[4]), -54,-36),
            ),
            N:(
                (self.gen_img(paths[5]), 0,0),
                (self.gen_img(paths[6]), -54,-36),
                (self.gen_img(paths[7]), -54,-36),
                (self.gen_img(paths[8]), -54,-36),
                (self.gen_img(paths[9]), -54,-36),
            ),
            E:(
                (self.gen_img(paths[10]), 0,0),
                (self.gen_img(paths[11]), -51,-36),
                (self.gen_img(paths[12]), -51,-36),
                (self.gen_img(paths[13]), -51,-36),
                (self.gen_img(paths[14]), -51,-36),
            ),
            W:(
                (pg.transform.flip(self.gen_img(paths[15]), True, False), 0,0),
                (self.gen_img(paths[16]), -57,-36),
                (self.gen_img(paths[17]), -57,-36),
                (self.gen_img(paths[18]), -57,-36),
                (self.gen_img(paths[19]), -57,-36),
            )}

        self.image = self.images[S][0][0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pg.mask.from_surface(self.image)
        self.counter = 1
        self.frame_counter = 0
        self.animate_frames = 0

            
    def use_animate(self, direction=S):
        if self.counter >= len(self.images[direction]): 
            self.counter = 0 # reset
            self.player.allow_move = True
            self.player.use_animate_bool = False
            self.kill()
        
        # load from item files
        self.player.image = self.gen_img(
                            "./sprites/player_sprite/larry_swing_E0.png")
        
        self.image = self.images[direction][self.counter][0]
        self.rect.x = self.player.rect.x +\
                        self.images[direction][self.counter][1]
        self.rect.y = self.player.rect.y +\
                        self.images[direction][self.counter][2]
        
        if self.frame_counter < self.animate_frames:
            self.frame_counter += 1
        else:
            self.frame_counter = 0
            self.counter += 1

        