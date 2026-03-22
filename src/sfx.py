import pygame as pg
from .node import Node


class SFX(Node):
    def setup(self):
        self.sound = pg.mixer.Sound(self.init.get("file"))
    
    def update(self):
        self.sound.set_volume(self.scene.game.sfx_volume / 10)
    
    def play(self, *args, **kwargs):
        self.sound.play(*args, **kwargs)


    def stop(self,):
        self.sound.stop()
