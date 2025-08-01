"""
file: src/input.py
"""
from dataclasses import dataclass

import pygame as pg
from .compass import Compass



DEAD_ZONE = 0.5
BUFFER_TIME = 250 # ms


class Input():

    def __init__(self, binds, *args, **kwargs):
        self.key_bind = binds.get("key_bind")
        self.ctlr_bind = binds.get("ctlr_bind")
        self.actions = []
        self.held = []
        self.last_actions = []

        self.controllers = [
            pg.joystick.Joystick(i)
            for i in range(pg.joystick.get_count())
        ]


    def update(self):
        self.ctlr_input(0)
        self.actions = self.keyboard_input()
        self.held = [
            action 
            for action in self.actions 
            if action in self.last_actions
        ]
        self.last_actions = self.actions
        
    
    def get(self):
        return self.actions, self.held


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
            button_state +  
            hat_state + 
            [round(val, 2) for val in axes_state]
        )
    
        return [float(val) for val in all_ctrl_inputs]


    def keyboard_input(self):
        pressed_keys = pg.key.get_pressed()
        game_input = [
            key for key, bind in self.key_bind.items()
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

