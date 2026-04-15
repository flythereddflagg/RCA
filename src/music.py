import pygame as pg

from .node import Node

# TODO -4- make music triggers for events (spagoot)

class Music(Node):

    def setup(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        self.filename = self.init.get("filename", "")
        if self.filename:
            self.load_play(self.filename, n_times=0, fade_ms=1000)
        


    
    def update(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        pg.mixer.music.set_volume(self.scene.game.music_volume / 10)

        if (
            self.loop_after > 0 
            and (pg.time.get_ticks() - self.start_time)/1000 > self.loop_after
        ):
            self.goto(self.then_goto)
            self.start_time = pg.time.get_ticks()
            

    def goto(time):
        pg.mixer.music.rewind()
        pg.mixer.music.set_pos(time)


    def deconstruct(self):
        self.stop()


    def load_play(filename, n_times=0, fade_ms):
        self.filename = filename
        pg.mixer.music.load(filename)
        pg.mixer.music.play(n_times-1, fade_ms=fade_ms)


    def stop(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()
    
    
    def play_loop(self, start, end):
        self.goto(start)
        self.then_goto = start
        self.loop_after = end - start
        self.start_time = pg.time.get_ticks()
    

    def exit_loop(self):
        self.goto(self.then_goto + self.loop_after)
        self.loop_off()
    

    def loop_off(self):
        self.start_time = -1
        self.loop_after = -1
        self.then_goto = -1
