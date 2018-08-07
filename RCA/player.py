"""
File     : player.py
Author   : Mark Redd

Player class. Should define all logic relating to the player.
"""
from constants import *
from rca_sprite import SpriteRCA

class Player(SpriteRCA):
    
    def __init__(self, eng):
        super().__init__()
        self.img_paths = [
            "./sprites/player_sprite/larry_st_N.png",
            "./sprites/player_sprite/larry_wk_N.png",
            "./sprites/player_sprite/larry_st_S.png",
            "./sprites/player_sprite/larry_wk1_S.png",
            "./sprites/player_sprite/larry_wk2_S.png",
            "./sprites/player_sprite/larry_st_EW.png",
            "./sprites/player_sprite/larry_wk1_EW.png",
            "./sprites/player_sprite/larry_wk2_EW.png"]
        self.original_size = (16,22)
        self.size_multiplier = 3
        self.size = (
            self.original_size[0] * self.size_multiplier, 
            self.original_size[1] * self.size_multiplier)
        self.images = (
            # stand, walk1, walk2
            (   self.gen_img(self.img_paths[0]),
                self.gen_img(self.img_paths[1]),
                pg.transform.flip(
                    self.gen_img(self.img_paths[1]), True, False)), # N
            
            (   self.gen_img(self.img_paths[5]),
                self.gen_img(self.img_paths[6]),
                self.gen_img(self.img_paths[7])), # E
            
            (   self.gen_img(self.img_paths[2]),
                self.gen_img(self.img_paths[3]),
                self.gen_img(self.img_paths[4])), # S
            
            (   pg.transform.flip(
                    self.gen_img(self.img_paths[5]), True, False),
                pg.transform.flip(
                    self.gen_img(self.img_paths[6]), True, False),
                pg.transform.flip(
                    self.gen_img(self.img_paths[7]), True,False))) # W

        self.eng = eng
        self.direction = S
        self.image = self.images[self.direction][0]
        self.rect = self.image.get_rect()
        self.rect.x = CENTERX
        self.rect.y = CENTERY
        self.mask = pg.mask.from_surface(self.image)
        self.counter = 0


    def walk_animate(self, direction):
        self.direction = direction
        self.image = self.images[direction][1]\
            if self.counter < PLAYERANIMATEFRAMES / 2\
            else self.images[direction][2]
        self.counter += 1
        if self.counter > PLAYERANIMATEFRAMES: self.counter = 0 # reset counter
    

    def stand(self):
        self.image = self.images[self.direction][0]

        
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

    def use_item_1(self):
        print("Using Item 1!")
    
    def use_item_2(self):
        print("Using item 2!")
        