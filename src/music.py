import pygame as pg

from .node import Node

class Music(Node):
    def __init__(self, filename, **options):
        super().__init__(**options)
        self.filename = filename
        self.sprite = None
        pg.mixer.music.load(self.filename)
        pg.mixer.music.play(-1) 

