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
        
        self.primary_loop = self.init.get("primary_loop", [])
        self.reset()

    
    def update(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        pg.mixer.music.set_volume(self.scene.game.music_volume / 10)

        if (
            self.end_after 
            and self.current_loop_time() > self.loop_after
        ):
            pg.mixer.music.stop()
            self.reset()

        elif (
            self.loop_after > 0 
            and self.current_loop_time() > self.loop_after):
            self.goto(self.then_goto)
            self.start_time = pg.time.get_ticks()
            
        elif (
            self.primary_loop 
            and self.current_loop_time() > self.primary_loop[1]
        ):
            self.play_loop(*self.primary_loop)


    def goto(self, time):
        pg.mixer.music.rewind()
        pg.mixer.music.set_pos(time)


    def deconstruct(self):
        self.stop()

    def current_loop_time(self):
        return (pg.time.get_ticks() - self.start_time)/1000

    def load_play(self, filename, n_times=0, fade_ms=0):
        pg.mixer.music.load(filename)
        pg.mixer.music.play(n_times-1, fade_ms=fade_ms)
        self.start_time = pg.time.get_ticks()


    def stop(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()
    
    
    def play_loop(self, start, end):
        self.goto(start)
        self.then_goto = start
        self.loop_after = end - start
        self.start_time = pg.time.get_ticks()
    

    def play_then_end(self, after):
        self.end_after = True
        self.loop_after = after


    def exit_loop(self):
        self.goto(self.then_goto + self.loop_after)
        self.reset()
    

    def reset(self):
        self.loop_after = -1
        self.then_goto = -1
        self.end_after = False
