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
        n_times = self.init.get("n_times", 0)
        fade_ms = self.init.get("fade_ms", 0)
        if self.filename:
            self.load_play(self.filename, n_times=n_times, fade_ms=fade_ms)
        
        self.primary_loop = self.init.get("primary_loop", [])
        self.reset()
        if self.primary_loop:
            self.play_loop(*primary_loop)
        

    
    def update(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        pg.mixer.music.set_volume(self.scene.game.music_volume / 10)

        if (
            self.end_after 
            and self.current_loop_time() > (self.end - self.start)
        ):
            pg.mixer.music.stop()
            self.reset()

        elif (
            self.end > 0 
            and self.current_loop_time() > (self.end - self.start)
        ):
            self.goto(self.then_goto)


    def goto(self, time):
        self.start = time
        pg.mixer.music.rewind()
        pg.mixer.music.set_pos(time)
        self.start_time = pg.mixer.music.get_pos()


    def deconstruct(self):
        self.stop()

    def current_loop_time(self):
        return (pg.mixer.music.get_pos() - self.start_time)/1000

    def load_play(self, filename, n_times=1, fade_ms=0):
        pg.mixer.music.load(filename)
        pg.mixer.music.play(n_times-1, fade_ms=fade_ms)
        self.start_time = pg.mixer.music.get_pos()


    def stop(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()
    
    
    def play_loop(self, start, end, then_goto=-1):
        assert end > start, \
            f"{type(self)} Error: invalid start and end in play_loop"
        self.goto(start)
        self.then_goto = start if then_goto >= 0 else then_goto
        self.end = end
    

    def play_then_end(self, end):
        self.end_after = True
        self.end = end


    def exit_loop(self):
        self.goto(self.end)
        self.reset()
    

    def reset(self):
        self.start = -1
        self.end = -1 
        self.then_goto = -1
        self.end_after = False
