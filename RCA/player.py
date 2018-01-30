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
        self.images = [
            pg.image.load(i).convert_alpha() 
            for i in range(len(self.img_paths))]
        self.image = self.images[1]
        #self.image = pg.image.load(
        #    "./sprites/player_sprite/player_sprite_facing_south.png"
        #    ).convert_alpha() # 12 X 22
        self.image = pg.transform.scale(self.image, (36, 66))
        #self.image = pg.Surface([60, 80])
        
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 100
    
    def moveRight(self, pixels):
        self.rect.x += pixels
 
    def moveLeft(self, pixels):
        self.rect.x -= pixels
 
    def moveDown(self, speed):
        self.rect.y += speed
 
    def moveUp(self, speed):
        self.rect.y -= speed
 
    def changeSpeed(self, speed):
        self.speed = speed