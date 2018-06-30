"""
File     : background.py
Author   : Mark Redd

Simple class to instatiate background graphics
"""
from rca_sprite import SpriteRCA
import pygame as pg

class Background(SpriteRCA):
    def __init__(self, xpos, ypos, img_path):
        super().__init__()
        self.image = pg.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
