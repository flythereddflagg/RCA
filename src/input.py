"""
file: src/input.py
"""
# TODO add fuzzy finding of controllers via the difflib
from dataclasses import dataclass
import re

import pygame as pg
from .compass import Compass



DEAD_ZONE = 0.5
BUFFER_TIME = 250 # ms


class Input():

    def __init__(self, parent, binds, *args, **kwargs):
        self.parent = parent
        self.key_bind = binds.get("key_bind")
        self.ctlr_bind = binds.get("ctlr_bind")
        self.inv_ctlr_bind = (
            {val:key for key, val in self.ctlr_bind.items()} 
            if self.ctlr_bind else None
        )
        self.binds = binds
        self.actions = []
        self.held = []
        self.last_actions = []

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

    def update(self):
        events = pg.event.get()
        if self.parent.settings.SHOW_EVENTS and events:
            print(events)
        for event in events:
            if event.type == pg.QUIT:
                self.actions = [("QUIT", 1.0)]
                return
        # player one only for now
        ctlr_input = self.map_ctlr_input(self.ctlr_input(0), 0) 
        self.actions:list[tuple[str, float]] = list(set(self.keyboard_input() + ctlr_input))
        self.held = [
            action 
            for action in self.actions 
            if action in self.last_actions
        ]
        self.last_actions = self.actions.copy()
        if self.parent.settings.SHOW_EVENTS and self.actions:
            print(self.actions, self.held)
        
    
    def get(self):
        return self.actions.copy(), self.held.copy()

    def map_ctlr_input(
        self, inputs:list[float], player:int
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
    
        return [float(val) for val in all_ctrl_inputs]


    def keyboard_input(self) -> list[tuple[str, float]]:
        pressed_keys = pg.key.get_pressed()
        game_input = [
            (key, 1.0) for key, bind in self.key_bind.items()
            if pressed_keys[pg.key.key_code(bind)]
        ]
        return game_input
    

    def event_input(self):
        # if you want to pass events you need to translate them
        # into game commands
        events = pg.event.get()
        event_inputs = []

        if self.SHOW_EVENTS:
            for event in events:
                print(event.type, event)
        if pg.QUIT in [event.type for event in events]: return ["QUIT"]

        return event_inputs

