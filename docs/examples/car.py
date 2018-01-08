import pygame as pg

WHITE = (255,255,255)

class Car(pg.sprite.Sprite):
    def __init__(self, color, width, height, speed):
        super(Car, self).__init__()
        
        self.image = pg.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        
        pg.draw.rect(self.image, color, [0,0,width,height])
        
        self.rect   = self.image.get_rect()
        self.width  = width
        self.height = height
        self.color  = color
        self.speed  = speed

    def moveRight(self,pixels):
        self.rect.x += pixels
    
    def moveLeft(self,pixels):
        self.rect.x -= pixels
    
    def moveForward(self, speed):
        self.rect.y += self.speed * speed / 20
    
    def moveBackward(self, speed):
        self.rect.y -= self.speed * speed / 20
    
    def changeSpeed(self, speed):
        self.speed = 20
    
    def repaint(self, color):
        self.color = color
        pg.draw.rect(self.image, self.color, [0,0,self.width, self.height])
        
