from rca_sprite import SpriteRCA
import pygame as pg

WHITE = (233,255,34)

class R1(SpriteRCA):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(
            "./sprites/player_sprite/player_sprite_facing_south.png"
            ).convert_alpha() # 12 X 22
        self.image = pg.transform.scale(self.image, (36, 66))
        #self.image = pg.Surface([60, 80])
        #self.image.fill(WHITE)
        #self.image.set_colorkey(WHITE)
        #pg.draw.rect(self.image, 
        #    (255,255,255,0), 
        #    [0, 0, 60, 80])
        
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