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
        self.input = Input(self)
        w, h = self.ASPECT_RATIO
        float_aspect_ratio = w / h

        self.SCREENWIDTH = (
            int(self.RESOLUTION * float_aspect_ratio) *
            self.SCALE
        )
        self.SCREENHEIGHT = self.RESOLUTION * self.SCALE
        

        self.screen = pg.display.set_mode(
            [self.SCREENWIDTH, self.SCREENHEIGHT], pg.RESIZABLE
        )
        self.clock = pg.time.Clock()

        

        self.load_scene(yaml_path=self.INITAL_SCENE, player=None)
        self.player = self.scene.node_from_dict(load_yaml(self.PLAYER))
        self.scene.place_node(self.player, self.scene.layers['foreground'])
        self.player.sprite.rect.center = self.PLAYER_START_POSITION
        if self.DEBUG:
            for sprite in self.scene.all_sprites.sprites():
                sprite.pos = pg.font.SysFont("Sans", 10)
        
        if self.FPS_COUNTER or self.DEBUG:
            self.fps_counter = pg.font.SysFont("Sans", 22)
        

    def load_scene(self, **kwargs) -> Scene:
        self.scene = Scene(game=self,  groups=self.SPRITE_GROUPS, **kwargs)
        if self.DEBUG:
            for sprite in self.scene.all_sprites.sprites():
                sprite.pos = pg.font.SysFont("Sans", 10)
        return self.scene

    def run(self):
        self.running = True

        while self.running:
            game_input = self.input.get()
            self.logic(game_input)
            self.input.update_held(game_input)
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
        if self.player:
            self.player.apply(game_input)

        # update everything in the scene
        if self.scene and not self.paused: 
            self.scene.update()


    def draw_frame(self):

        self.screen.fill(BLACK)
        for group_name in self.scene.data.DRAW_LAYERS:
            self.scene.layers[group_name].draw(self.screen)

        if self.FPS_COUNTER or self.DEBUG:
            fps = str(int(self.clock.get_fps()))
            fps_sprite = self.fps_counter.render(fps, True, (255,255,255))
            self.screen.blit(fps_sprite, (10,10))
        
        if self.DEBUG:
            background = self.scene.layers['background'].sprites()[0]
            for group_name in self.scene.data.DRAW_LAYERS:
                sprites = self.scene.layers[group_name].sprites()
                for sprite in sprites:
                    pg.draw.rect(
                        self.screen, (255,255,255), sprite.rect, width=2
                    )
                    pos1, pos2 = (
                        str(sprite.rect.topleft), str(
                            pg.math.Vector2(sprite.rect.topleft) - 
                            pg.math.Vector2(background.rect.topleft)
                        ),
                    )
                    pos_sprite = sprite.pos.render(
                        f"{pos1} ; {pos2}", 
                        True, (255,255,255)
                    )
                    self.screen.blit(
                        pos_sprite, 
                        pg.math.Vector2(sprite.rect.topleft) - (0, 15)
                    )
        
        pg.display.flip()

