"""
file: src/input.py
"""
from dataclasses import dataclass

import pygame as pg
from .compass import Compass

DEAD_ZONE = 0.5
BUFFER_TIME = 250 # ms


class Input():

    def __init__(self):

    def update(self):
    
    def get(self):
        # return [action for action in self.buffer.keys()]
        inputs = list(self.buffer.keys())

        if self.REPLAY is None:
            if self.LOG_INPUT:
                self.input_record.append(inputs)
            return inputs
        else:
            if 'QUIT' in inputs:
                return inputs
            inputs = [
                thing 
                for thing in next(self.lines).strip().split('|') 
                if thing
            ]
            return inputs


    def update_held(self, all_input):
        self.held = {key:False for key in self.held.keys()}
        # breakpoint()
        for held_action in all_input:
            if isinstance(held_action, tuple):
                held_action, _ = held_action
            assert held_action in self.held, f"Invalid action: '{held_action}'"
            self.held[held_action] = True


    def ctlr_input(self, player):
        if not self.controllers: return []
        axes = [
            self.controllers[player].get_axis(i) 
            for i in range(self.controllers[player].get_numaxes())
        ]
        
        button_states = [
            self.controllers[player].get_button(i) 
            for i in range(self.controllers[player].get_numbuttons())
        ]
        
        self.controller_state = button_states + [round(val, 3) for val in axes]
        button_input = [
            key for key, bind in self.ctlr_bind.items()
            if bind in self.controller_buttons and
            button_states[self.controller_buttons[bind]]
        ]
        axes_input = []
        for key, bind in self.ctlr_bind.items():
            ax, sign = bind[:-1], bind[-1]
            if ax in self.controller_axes:
                one = int(sign + '1')
                ax_value = round(axes[self.controller_axes[ax]], 1)
                ax_value = ax_value if abs(ax_value) > DEAD_ZONE else 0.0
                # ax_value is not 0 and one and ax_value are the same sign
                if (ax_value * one) > 0:
                    axes_input.append((key, ax_value))

        if self.SHOW_EVENTS and axes_input: print(axes_input)
        

        return button_input + axes_input


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

