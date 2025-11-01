import pygame as pg
import sys

from .node import Node

# TODO -2- make music triggers for events (spagoot)

class Music(Node):

    def setup(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        self.filename = self.init.get("filename")
        assert self.filename, "No filename given"
        # for wasm build
        # if sys.platform == "emscripten":
        self.filename = self.filename.replace(".ogg", "-pygbag.ogg")
        self.measure_counter = 0.0
        # total measures that have played per music.get_pos
        self.last_update = 0.0 
        self.measure_time = 1.846
        seq_list = self.init.get("sequence")
        if seq_list is not None:
            self.sequence = iter(seq_list)
            self.cur = next(self.sequence)
            self.measure_time = self.init.get("measure_time", 1.0)
        else:
            self.sequence = None
            self.cur = None
            self.measure_time = None


        pg.mixer.music.load(self.filename)
        pg.mixer.music.play(-1, fade_ms=1000)
 
    
    def update(self):
        if (
            self.scene.game.settings["DEBUG"] 
            and not self.scene.game.settings["MUSIC"]
        ):
            return
        if self.sequence is None: return
        
        ms_elapsed = pg.mixer.music.get_pos()
        self.measure_counter = (
            ms_elapsed
            / 1000.0 
            / self.measure_time
        ) - self.last_update
        # print(self.measure_counter)
        if self.measure_counter >= self.cur[0]:
            trigger, action, target = self.cur
            next_ = next(self.sequence, None)
            self.cur = self.cur if next_ is None else next_
            self.last_update = (
                ms_elapsed
                / 1000.0 
                / self.measure_time
            )
            # print(
            #     trigger, action, target, 
            #     self.measure_time, 
            #     target * self.measure_time
            # )
            if action == "goto":
                pg.mixer.music.rewind()
                pg.mixer.music.set_pos(target * self.measure_time)



    def deconstruct(self):
        self.stop()


    def stop(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()