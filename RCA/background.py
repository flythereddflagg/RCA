"""
File     : background.py
Author   : Mark Redd

Simple class to instantiate background graphics
"""
from rca_sprite import SpriteRCA
import pygame as pg

class Background(SpriteRCA):
    def __init__(self, image_path, xposition, yposition):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xposition
        self.rect.y = yposition
        self.width = self.image.get_width()
        self.height = self.image.get_height()
