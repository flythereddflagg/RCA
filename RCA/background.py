from rca_sprite import SpriteRCA
import pygame as pg

class Bg1(SpriteRCA):
    def __init__(self, xpos, ypos):
        super().__init__()
        img_path = "./sprites/backgrounds/trail_ew.png"
        self.image = pg.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
