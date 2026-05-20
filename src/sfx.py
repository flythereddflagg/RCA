import pygame as pg
from .node import Node


class SFX(Node):
    def setup(self):
        self.sound = pg.mixer.Sound(self.init.get("file"))
        self.length = 0
        self.start_time = 0
    
    def update(self):
        self.sound.set_volume(self.scene.game.sfx_volume / 10)
        # print(self.length, self.start_time, (pg.time.get_ticks() - self.start_time)/1000)
        if (
            self.length 
            and (pg.time.get_ticks() - self.start_time)/1000 > self.length
        ):
            breakpoint()
            pg.mixer.music.unpause()
            self.length = 0

    
    def play(self, *args, **kwargs):
        self.sound.play(*args, **kwargs)

    
    def pause_play(self, *args, **kwargs):
        # TODO -4- get pause play to work?
        self.length = self.sound.get_length()
        self.start_time = pg.time.get_ticks()
        pg.mixer.music.pause()
        self.sound.play(*args, **kwargs)
        


    def stop(self,):
        self.sound.stop()
