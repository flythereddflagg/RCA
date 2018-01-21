from rca_sprite import SpriteRCA
import pygame as pg

WHITE = (233,255,34)

class R1(SpriteRCA):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([60, 80])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pg.draw.rect(self.image, 
            (100,23,232), 
            [0, 0, 60, 80])
        
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 100
    
    def moveRight(self, pixels):
        self.rect.x += pixels
 
    def moveLeft(self, pixels):
        self.rect.x -= pixels
 
    def moveForward(self, speed):
        self.rect.y += self.speed * speed / 20
 
    def moveBackward(self, speed):
        self.rect.y -= self.speed * speed / 20
 
    def changeSpeed(self, speed):
        self.speed = speed