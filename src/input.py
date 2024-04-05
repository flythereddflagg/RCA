"""
file: src/input.py
"""
import pygame as pg
from .compass import Compass

DEAD_ZONE = 0.5

class Input():

    def __init__(self, game):
        self.game = game
        self.KEY_BIND = self.game.KEY_BIND
        self.CTLR_BIND = self.game.CTLR_BIND
        self.CTLR_BUTTON = self.game.CTLR_BUTTON
        self.CTLR_AXES = self.game.CTLR_AXES
        self.SHOW_EVENTS = self.game.SHOW_EVENTS
        self.held = {
            **{key:False for key in self.KEY_BIND.keys()},
            **{key:False for key in self.CTLR_BIND.keys()}
        }
        self.controller_buttons = {
            name: index 
            for index, name in enumerate(self.game.CTLR_BUTTON.split(','))
        }
        self.controller_axes = {
            name: index 
            for index, name in enumerate(self.game.CTLR_AXES.split(','))
        }
        
        # detect and load controllers
        self.controllers = []
        for i in range(0, pg.joystick.get_count()):
            self.controllers.append(pg.joystick.Joystick(i))
            self.controllers[-1].init()
            controllers  = self.controllers
            print (f"Detected controller: {controllers[-1].get_name()}")
            print(f"{controllers[-1].get_numbuttons()} buttons detected")
            print(f"{controllers[-1].get_numhats()} joysticks detected")
        print(f"{len(self.controllers) + 1} input devices detected")
        print(f"\t- 1 keyboard + {len(self.controllers)} controllers")


    def get(self):

        # INFO this only allows for one player currently
        keyboard_input = self.keyboard_input()
        ctlr_input = []
        event_input = self.event_input()
        # mouse_input = [] # no mouse input for RCA
  
        if self.controllers: 
            player = 0 # player index 0
            ctlr_input = self.ctlr_input(player)

        # set to erase duplicate inputs
        all_input = list(set(ctlr_input + keyboard_input + event_input))

        if self.SHOW_EVENTS and all_input: 
            print("input:", all_input, end=';')
            print("held:", [key for key, held in self.held.items() if held])
        if 'QUIT' in all_input: return ['QUIT']

        return all_input


    def update_held(self, all_input):
        self.held = {key:False for key in self.held.keys()}
        # breakpoint()
        for held_action in all_input:
            if isinstance(held_action, tuple):
                held_action, _ = held_action
            assert held_action in self.held, f"Invalid action: '{held_action}'"
            self.held[held_action] = True


    def ctlr_input(self, player):
        axes = [
            self.controllers[player].get_axis(i) 
            for i in range(self.controllers[player].get_numaxes())
        ]
        button_states = [
            self.controllers[player].get_button(i) 
            for i in range(self.controllers[player].get_numbuttons())
        ]
        button_input = [
            key for key, bind in self.CTLR_BIND.items()
            if bind in self.controller_buttons and
            button_states[self.controller_buttons[bind]]
        ]
        axes_input = []
        for key, bind in self.CTLR_BIND.items():
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
            key for key, bind in self.KEY_BIND.items()
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