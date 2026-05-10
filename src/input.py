"""
file: src/input.py
"""
from dataclasses import dataclass
import re

import pygame as pg
import pygame._sdl2.controller as pg_sdl2_controller
from .compass import Compass


SDL2_MIN, SDL2_MAX = -32768, 32768
DEAD_ZONE = 0.5
BUFFER_TIME = 250 # ms
USE_SDL2_CTLR = True


class Input():

    def __init__(self, parent, binds, *args, **kwargs):
        self.parent = parent
        self.binds = binds
        self.key_bind = self.binds.get("key_bind")
        self.actions = []
        self.held = []
        self.last_actions = []
        self.controllers = []
        self.sdl2_controllers = []
        if USE_SDL2_CTLR:
            self.sdl2_controller_setup()
        else:
            self.ctlr_setup()


    def clear(self):
        self.actions = []
        self.held = []
        self.last_actions = []


    def sdl2_controller_setup(self):
        self.sdl2_controller_bind = self.binds.get("SDL2 Controller Bind")
        self.sdl2_consts = {
            key: val
            for key, val in vars(pg).items()
            if "CONTROLLER_" in key
        }
        self.sdl2_controllers = []
        if not pg_sdl2_controller.get_init():
            pg_sdl2_controller.init()

        print("Controllers connected:")
        for i in range(pg_sdl2_controller.get_count()):
            print(
                # commented out because name_forindex is missing.
                # f"\t Name: {pg_sdl2_controller.name_forindex(i)};",
                f"Valid = {pg_sdl2_controller.is_controller(i)}"
            )
            self.sdl2_controllers.append(pg_sdl2_controller.Controller(i))


    def ctlr_setup(self):
        self.ctlr_bind = self.binds.get("ctlr_bind")
        self.inv_ctlr_bind = (
            {val:key for key, val in self.ctlr_bind.items()} 
            if self.ctlr_bind else None
        )

        self.controllers = [
            pg.joystick.Joystick(i)
            for i in range(pg.joystick.get_count())
        ]
        controller_names = [
            ctlr.get_name()
            for ctlr in self.controllers
        ]
        mapping_str = [
            self.binds[name] 
            if name in self.binds 
            else self.binds["Generic"]
            for name in controller_names
        ]
        self.controller_mappings = [
            re.split(r"[\s]+", map_string.strip())
            for map_string in mapping_str
        ]

    def hot_plug_check(self):
        if USE_SDL2_CTLR:
            current = self.sdl2_controllers
            check = pg_sdl2_controller.get_count
            setup = self.sdl2_controller_setup
        else:
            current = self.controllers
            check = pg.joystick.get_count
            setup = self.ctlr_setup
        
        if len(current) != check():
            setup()


    def update(self):
        # TODO -3- add more player controls player one only for now
        self.hot_plug_check()
        player_number = 0
        events = pg.event.get()
        if self.parent.settings.SHOW_EVENTS and events:
            print(events)
        for event in events:
            if event.type == pg.QUIT:
                self.actions = [("QUIT", 1.0)]
                return

        self.actions:list[tuple[str, float]] = list(set(
            self.keyboard_input() 
            + self.sdl2_controller_input(player_number)
            + self.ctlr_input(player_number)
            # + self.event_input(player_number)
        ))
        self.held = [
            action
            for action, val in self.actions 
            if action in [a for a, _ in self.last_actions]
        ]
        self.last_actions = self.actions.copy()
        if self.parent.settings.SHOW_EVENTS and self.actions:
            print(self.actions, self.held)
        
    
    def new_actions(self):
        actions, held = self.get()
        return [action for action, _ in actions if action not in held]


    def get(self):
        return self.actions.copy(), self.held.copy()


    def keyboard_input(self) -> list[tuple[str, float]]:
        pressed_keys = pg.key.get_pressed()
        game_input = [
            (key, 1.0) for key, bind in self.key_bind.items()
            if pressed_keys[pg.key.key_code(bind)]
        ]
        return game_input
    

    # def event_input(self):
    #     # if you want to pass events you need to translate them
    #     # into game commands
    #     events = pg.event.get()
    #     event_inputs = []

    #     if self.SHOW_EVENTS:
    #         for event in events:
    #             print(event.type, event)
    #     if pg.QUIT in [event.type for event in events]: return ["QUIT"]

    #     # return event_inputs
    #     return []


    def sdl2_controller_input(self, player:int):
        if not self.sdl2_controllers: return []
        controller = self.sdl2_controllers[player]
        actions = []
        for action, bind in self.sdl2_controller_bind.items():
            if (
                "BUTTON" in bind and 
                controller.get_button(self.sdl2_consts[bind])
            ):
                actions.append((action, 1.0))
            elif "AXIS" in bind:
                axis_val = controller.get_axis(self.sdl2_consts[bind[:-1]])
                if axis_val < 0 and bind[-1] == "-":
                    norm = axis_val/SDL2_MIN
                elif axis_val >= 0 and bind[-1] == "+":
                    norm = axis_val/SDL2_MAX
                else: 
                    continue
                if abs(norm) >= DEAD_ZONE:
                    actions.append((action, abs(norm)))
        
        # TODO -4- this is a hackey solution but will allow Dpad to be read as if it is joystick
        actions = [
            (action[2:], val) if action.startswith("D_")
            else (action, val)
            for action, val in actions
        ]
        ###
        return actions


    def ctlr_input(self, player:int) -> list[float]:

        if not self.controllers: return []
        axes_state = [
            self.controllers[player].get_axis(i) 
            for i in range(self.controllers[player].get_numaxes())
        ]
        
        button_state = [
            self.controllers[player].get_button(i) 
            for i in range(self.controllers[player].get_numbuttons())
        ]
        hat_state = [
            hatval
            for i in range(self.controllers[player].get_numhats())
            for hatval in self.controllers[player].get_hat(i)
        ]
        all_ctrl_inputs = (
            [round(val, 2) for val in axes_state] +
            button_state +  
            hat_state
        )
    
        return self.map_ctlr_input(
            [float(val) for val in all_ctrl_inputs], 
            player
        )


    def map_ctlr_input(
        self, 
        inputs:list[float], 
        player:int
    ) -> list[tuple[str, float]]:

        if not inputs: return []
        
        mapping = [
            list(item) 
            for item in zip(self.controller_mappings[player], inputs)
        ]
        for i, inps in enumerate(mapping):
            inp, val = inps
            if 'x' in inp or 'y' in inp:
                inp = inp + "-" if val < 0.0 else inp + "+"
                mapping[i] = [inp, val]

        actions = [
            (self.inv_ctlr_bind.get(action), value) 
            for action, value in mapping 
            if abs(value) > DEAD_ZONE and action in self.inv_ctlr_bind
        ]
        return actions