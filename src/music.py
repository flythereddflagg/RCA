import pygame as pg

from .node import Node

class Music(Node):

    def setup(self)
        self.filename = self.init.get("filename")
        assert self.filename, "No filename given"
        self.sprite = None
        pg.mixer.music.load(self.filename)
        pg.mixer.music.play(-1)
    
    def update(self):
        pass

