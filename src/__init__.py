"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""

import pygame as pg
import collections

from .dict_obj import DictObj
from .scene import Scene
from .tools import load_yaml
from .input import Input

BLACK = (0, 0, 0)
ASPECT_RATIO = 16 / 9


class GameState(DictObj):
    """
    connects the hardware to game logic and holds the game state
    including the scenes
    """
    def __init__(self, data_path):
        init_data = load_yaml(data_path)
        super().__init__(**init_data)
        self.dt = 1
        self.running = False
        self.paused = False
        self.scene = None
        self.SCREENWIDTH = (
            int(int(self.RESOLUTION[:-1]) * ASPECT_RATIO) *
            self.SCALE
        )
        self.SCREENHEIGHT = int(self.RESOLUTION[:-1]) * self.SCALE
        self.input = Input(self)

        self.screen = pg.display.set_mode(
            [self.SCREENWIDTH, self.SCREENHEIGHT], pg.RESIZABLE
        )
        self.clock = pg.time.Clock()
        self.scene = Scene(self, self.INITAL_SCENE, self.PLAYER)
        
        if self.FPS_COUNTER:
            self.fps_counter = pg.font.SysFont("Sans", 22)

    def load_scene(self, *args, **kwargs):
        self.scene = Scene(*args, **kwargs)
        return self.scene

    def run(self):
        self.running = True

        while self.running:
            game_input = self.input.get()
            self.logic(game_input)
            self.draw_frame()
            self.dt = (
                self.clock.tick() 
                if self.FPS < -1 else 
                self.clock.tick(self.FPS)
            )



    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
            self.running = False
            return

        # apply all the input
        if self.scene.player:
            self.scene.player.apply(game_input)

        # update everything in the scene
        if self.scene and not self.paused: 
            self.scene.update()


    def draw_frame(self):

        self.screen.fill(BLACK)
        for group_name in self.scene.data.DRAW_LAYERS:
            self.scene.layers[group_name].draw(self.screen)

        if self.FPS_COUNTER:
            fps = str(int(self.clock.get_fps()))
            fps_sprite = self.fps_counter.render(fps, True, (255,255,255))
            self.screen.blit(fps_sprite, (10,10))
        
        pg.display.flip()

