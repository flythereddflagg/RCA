"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""

import pygame as pg
import collections

from .scene import Scene
from .tools import load_yaml
from .input import Input
from .node import node_from_dict

BLACK = (0, 0, 0)
# TODO make a scene manager that loads a bunch of scenes here and then loads them into the game and remembers them.

class GameState():
    """
    connects the hardware to game logic and holds the game state
    including the scenes
    """
    def __init__(self, data_path, REPLAY=None):
        self.settings:'.dictobj.DictObj' = load_yaml(data_path)
        self.dt = 1
        self.running = False
        self.paused = False
        self.scene = None
        self.saved_scenes = {}
        self.REPLAY = REPLAY
        self.screen = self.init_screen()
        self.clock = pg.time.Clock()
        self.fps_counter = (
            pg.font.SysFont("Sans", 22) 
            if self.settings.FPS_COUNTER or self.settings.DEBUG
            else None
        )
        self.input = Input(self)
        
        self.load_scene(yaml_path=self.settings.INITAL_SCENE)


    def init_screen(self):
        w, h = self.settings.ASPECT_RATIO
        float_aspect_ratio = w / h

        self.screenwidth, self.screenheight = (
            int(self.settings.RESOLUTION * float_aspect_ratio) *
            self.settings.SCALE,
            self.settings.RESOLUTION * self.settings.SCALE
        )        

        return pg.display.set_mode(
            [self.screenwidth, self.screenheight], pg.RESIZABLE
        )


    def load_scene(self, **init) -> Scene:
        self.scene = Scene(
            game=self,  groups=self.settings.SPRITE_GROUPS, **init
        )

        return self.scene # return reference to scene if needed


    def run(self):
        self.running = True

        while self.running:
            self.input.update()
            self.logic()
            self.draw_frame()
            self.dt = (
                self.clock.tick() 
                if self.settings.FPS < -1 else 
                self.clock.tick(self.settings.FPS)
            )


    def logic(self):
        # run all game logic here
        # quit overrides everything else
        game_input = self.input.get()
        if "QUIT" in game_input:
            self.running = False
            return

        # key to refresh scene
        if (
            "REFRESH" in game_input and 
            not self.input.held["REFRESH"] and 
            self.settings.DEBUG and 
            self.scene
        ):
            self.scene.refresh()

        # update everything in the scene
        if self.scene and not self.paused: 
            self.scene.update()


    def draw_frame(self):

        self.screen.fill(BLACK)
        for group_name in self.scene.draw_layers:
            self.scene.groups[group_name].draw(self.screen) 
        
        if self.settings.DEBUG:
            self.render_debug()
        
        pg.display.flip()



    def render_debug(self):
        if self.settings.FPS_COUNTER:
            fps = str(int(self.clock.get_fps()))
            fps_sprite = self.fps_counter.render(fps, True, (255,255,255))
            self.screen.blit(fps_sprite, (10,10))
            
        background = self.scene.background.sprites()[0] 
        for group_name in self.scene.draw_layers:
            sprites = self.scene.groups[group_name].sprites()
            for sprite in sprites:
                if not vars(sprite).get('pos'):
                    sprite.pos = pg.font.SysFont("Sans", 10)
                pg.draw.rect(
                    self.screen, (255,255,255), sprite.rect, width=2
                )
                pos1, pos2 = (
                    str(pg.math.Vector2(sprite.rect.topleft)//self.settings.SCALE), 
                    str((
                        pg.math.Vector2(sprite.rect.topleft) - 
                        pg.math.Vector2(background.rect.topleft)
                    )//self.settings.SCALE)
                )
                pos_sprite = sprite.pos.render(
                    f"{pos1} ; {pos2}", 
                    True, (255,255,255)
                )
                self.screen.blit(
                    pos_sprite, 
                    pg.math.Vector2(sprite.rect.topleft) - (0, 15)
                )
                if self.settings.SHOW_MASK and sprite.mask:
                    if (
                        not self.settings.SHOW_BG_MASK and 
                        sprite in self.scene.background
                    ): continue
                    self.screen.blit(
                        sprite.mask.to_surface(setcolor = (0,0,255,255), unsetcolor = None),
                        sprite.rect.topleft
                    )
                    