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
        # self.INV_KEY_BIND = {v: k for k, v in self.KEY_BIND.items()}
        self.controllers = []
        self.SCREENWIDTH = int(int(self.RESOLUTION[:-1]) * ASPECT_RATIO)
        self.SCREENHEIGHT = int(self.RESOLUTION[:-1])
        self.controller_buttons = {
            name: index 
            for index, name in enumerate(self.CTLR_BUTTON.split(','))
        }
        self.controller_axes = {
            name: index 
            for index, name in enumerate(self.CTLR_AXES.split(','))
        }
        
        # detect and load controllers
        for i in range(0, pg.joystick.get_count()):
            self.controllers.append(pg.joystick.Joystick(i))
            self.controllers[-1].init()
            controllers  = self.controllers
            print (f"Detected controller: {controllers[-1].get_name()}")
            print(f"{controllers[-1].get_numbuttons()} buttons detected")
            print(f"{controllers[-1].get_numhats()} joysticks detected")

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
            game_input = self.get_input()
            self.logic(game_input)
            self.draw_frame()
            self.dt = (
                self.clock.tick() 
                if self.FPS < -1 else 
                self.clock.tick(self.FPS)
            )


    def get_input(self):
        game_input = []

        events = pg.event.get()
        if self.SHOW_EVENTS:
            for event in events:
                print(event.type, event)
        if pg.QUIT in [event.type for event in events]: return ["QUIT"]    

        # TODO make the input more sophisticated
        pressed_keys = pg.key.get_pressed()
        game_input = [
            key for key, bind in self.KEY_BIND.items()
            if pressed_keys[pg.key.key_code(bind)]
        ]
        if self.controllers:
            PLAYER1 = 0
            axes = [
                self.controllers[PLAYER1].get_axis(i) 
                for i in range(self.controllers[PLAYER1].get_numaxes())
            ]
            button_states = [
                self.controllers[PLAYER1].get_button(i) 
                for i in range(self.controllers[PLAYER1].get_numbuttons())
            ]
            game_input += [ # add in button input
                key for key, bind in self.CTLR_BIND.items()
                if bind in self.controller_buttons and
                button_states[self.controller_buttons[bind]]
            ]
            axes_input = [ # add in joystick input
                key, bind for key, bind in self.CTLR_BIND.items()
                if bind[:3] in self.controller_axes and
                abs(axes[self.controller_axes[bind[:3]]]) > 0.01
            ]
            game_input += [

            ]

        if self.SHOW_EVENTS and game_input: print(game_input)
        if 'FORCE_QUIT' in game_input: return ['QUIT']
        
        return game_input


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
