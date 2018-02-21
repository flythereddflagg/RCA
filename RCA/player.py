from rca_sprite import SpriteRCA
from constants import *

class Player(SpriteRCA):
    
    def __init__(self, eng):
        super().__init__()
        self.img_paths = [
            "./sprites/player_sprite/larry_st_N.png",
            "./sprites/player_sprite/larry_st_S.png",
            "./sprites/player_sprite/larry_st_EW.png",
            "./sprites/player_sprite/larry_wk_N.png",
            "./sprites/player_sprite/larry_wk_S.png",
            "./sprites/player_sprite/larry_wk1_EW.png",
            "./sprites/player_sprite/larry_wk2_EW.png",
            ]
        self.image_list = [ # originally they were (16,22)
            pg.transform.scale(
            pg.image.load(i).convert_alpha(), (48, 66))
            for i in self.img_paths]
        self.image = self.image_list[1]
        self.rect = self.image.get_rect()
        self.rect.x = CENTERX
        self.rect.y = CENTERY
        self.counter = 0
        self.eng = eng
        self.direction = S
        self.standing = [
            self.image_list[0],
            self.image_list[2],
            self.image_list[1],
            pg.transform.flip(self.image_list[2],True,False)]
        self.consts = (
            # stand, walk1, walk2
            (   self.image_list[0],
                self.image_list[3],
                pg.transform.flip(self.image_list[3],True,False)), # N
            
            (   self.image_list[2],
                self.image_list[6],
                self.image_list[5]), # E
            
            (   self.image_list[1],
                self.image_list[4],
                pg.transform.flip(self.image_list[4],True,False)), # S
            
            (   pg.transform.flip(self.image_list[2],True,False),
                pg.transform.flip(self.image_list[6],True,False),
                pg.transform.flip(self.image_list[5],True,False))) # W

    def walk_animate(self, direction):
        self.direction = direction
        self.image = self.consts[direction][1]\
            if self.counter < PLRANIRT / 2\
            else self.consts[direction][2]
        self.counter += 1
        if self.counter > PLRANIRT: self.counter = 0 # reset counter

    
    def stand(self):
        #self.cam_correct()
        self.image = self.standing[self.direction]

