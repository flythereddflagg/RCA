from rca_sprite import SpriteRCA
import pygame as pg

class Player(SpriteRCA):
    def __init__(self):
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
        self.rect.x = 160
        self.rect.y = 100
        self.counter = 0
        self.direction = 0 # 0:N 1:E 2:S 3:W 
        self.standing = [
            self.image_list[0],
            self.image_list[2],
            self.image_list[1],
            pg.transform.flip(self.image_list[2],True,False)]
    
    
    def moveRight(self, pixels):
        self.direction = 1
        self.image = self.image_list[6]\
            if self.counter < 5 else\
            self.image_list[5]
        self.counter += 1
        if self.counter > 10: self.counter = 0
        self.rect.x += pixels
 
    def moveLeft(self, pixels):
        self.direction = 3
        self.image = pg.transform.flip(
            self.image_list[6],True,False)\
            if self.counter < 5 else\
            pg.transform.flip(
            self.image_list[5],True,False)
        self.counter += 1
        if self.counter > 10: self.counter = 0
        self.rect.x -= pixels
 
    def moveDown(self, speed):
        self.direction = 2
        self.image = pg.transform.flip(
            self.image_list[4],True,False)\
            if self.counter < 5 else\
            self.image_list[4]
        self.counter += 1
        if self.counter > 10: self.counter = 0
        self.rect.y += speed
 
    def moveUp(self, speed):
        self.direction = 0
        self.image = pg.transform.flip(
            self.image_list[3],True,False)\
            if self.counter < 5 else\
            self.image_list[3]
        self.counter += 1
        if self.counter > 10: self.counter = 0
        self.rect.y -= speed
 
    def changeSpeed(self, speed):
        self.speed = speed
    
    def stand(self):
        self.image = self.standing[self.direction]