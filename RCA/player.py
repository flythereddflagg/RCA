from rca_sprite import SpriteRCA
import pygame as pg

class Player(SpriteRCA):
    
    def __init__(self, bgs):
        super().__init__()
        self.img_paths = [
            "./sprites/player_sprite/player_sprite_facing_north.png",
            "./sprites/player_sprite/player_sprite_facing_south.png",
            "./sprites/player_sprite/player_sprite_facing_east_west.png",
            "./sprites/player_sprite/player_sprite_walking_north.png",
            "./sprites/player_sprite/player_sprite_walking_south.png",
            "./sprites/player_sprite/player_sprite_walking_east_west_1.png",
            "./sprites/player_sprite/player_sprite_walking_east_west_2.png",
            ]
        self.image_list = [ # originally they were (12,22)
            pg.transform.scale(
            pg.image.load(i).convert_alpha(), (36, 66))
            for i in self.img_paths]
        self.image = self.image_list[1]
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.counter = 0
        self.bgs = bgs
        self.direction = 0 # 0:N 1:E 2:S 3:W 
        self.standing = [
            self.image_list[0],
            self.image_list[2],
            self.image_list[1],
            pg.transform.flip(self.image_list[2],True,False)]
        self.CAMERASLACK = 100
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
                pg.transform.flip(self.image_list[5],True,False)), # W
        )
    
    
    def mv_bgs(self,pixels, dr=None):
        if dr == None: dr = self.direction
        for i in self.bgs.sprites():
            if dr == 0:
                i.rect.y += pixels
            elif dr == 1:
                i.rect.x -= pixels
            elif dr == 2:
                i.rect.y -= pixels
            elif dr == 3:
                i.rect.x += pixels
        
    
    def move(self, pixels, dir):
        self.direction = dir
        self.image = self.consts[dir][1]\
            if self.counter < 5 else\
            self.consts[dir][2]
        self.counter += 1
        if self.counter > 10: self.counter = 0
        if self.rect.x < 400 - self.CAMERASLACK or\
            self.rect.x > 400 + self.CAMERASLACK or\
            self.rect.y < 300 - self.CAMERASLACK or\
            self.rect.y > 300 + self.CAMERASLACK:
            self.mv_bgs(pixels)
            #self.cam_correct()
        else:
            if dir == 0:
                self.rect.y -= pixels
            elif dir == 1:
                self.rect.x += pixels
            elif dir == 2:
                self.rect.y += pixels
            elif dir == 3:
                self.rect.x -= pixels
    
    def cam_correct(self):
        while self.rect.x < 400 - self.CAMERASLACK or\
                self.rect.x > 400 + self.CAMERASLACK or\
                self.rect.y < 300 - self.CAMERASLACK or\
                self.rect.y > 300 + self.CAMERASLACK:
            if self.rect.y > 300 + self.CAMERASLACK:
                self.rect.y -= 1
                self.mv_bgs(1,2)
            if self.rect.y < 300 - self.CAMERASLACK:
                self.rect.y += 1
                self.mv_bgs(1,0)
            
            if self.rect.x > 400 + self.CAMERASLACK:
                self.rect.x -= 1
                self.mv_bgs(1,1)
            if self.rect.x < 400 - self.CAMERASLACK:
                self.rect.x += 1
                self.mv_bgs(1,3)
    
    def stand(self):
        self.cam_correct()
        self.image = self.standing[self.direction]

