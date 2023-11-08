"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""
import pygame as pg
import yaml
from .game_state import GameState

BLACK = (0,0,0)

def init_game(data_path):
    pg.init()
    controllers = []

    # detect and load controllers
    for i in range(0, pg.joystick.get_count()):
        controllers.append(pg.joystick.Joystick(i))
        controllers[-1].init()
        print (f"Detected controller: {controllers[-1].get_name()}")
        print(f"{controllers[-1].get_numbuttons()} buttons detected")
        print(f"{controllers[-1].get_numhats()} joysticks detected")


    with open(data_path) as f:
        raw_yaml = f.read()

    yaml_data = yaml.load(raw_yaml, Loader=yaml.Loader)
    game = GameState(**yaml_data)
    game.clock = pg.time.Clock()
    game.screen = pg.display.set_mode(game.SCREENSIZE)
    game.controllers = controllers
    game.INV_KEY_BINDINGS = {
        item:key for key, item in game.KEY_BINDINGS.items()
    }

    print(game.KEY_BINDINGS)

    return game


def run_game(game):
    game.running = True
    game_clock = pg.time.Clock()

    while game.running:
        game_input = get_input(game)
        if game_input: print(game_input)
        game.logic(game_input)
        draw_frame(game)
        
        game.clock.tick(game.FPS)
    pg.display.quit()
    pg.quit()


def get_input(game):
    game_input = []

    # make the exit button work
    events = pg.event.get()
    if pg.QUIT in [event.type for event in events]: return ["QUIT"]    

    # get general events
    # for event in events:
    #     print(event.type, event)

    # get pressed keyboard keys
    # TODO make the input more sophisticated
    valid_keys = game.INV_KEY_BINDINGS.keys()
    pressed_keys = [
        i 
        for i, pressed in enumerate(pg.key.get_pressed()) 
        if (pressed and i in valid_keys)
    ]
    # if pressed_keys: print(pressed_keys)

    if game.KEY_BINDINGS['FORCE_QUIT'] in pressed_keys: return ['QUIT']

    game_input = [
        game.INV_KEY_BINDINGS[pressed_key]
        for pressed_key in pressed_keys
    ]
    
    return game_input


def draw_frame(game):
    
    game.screen.fill(BLACK)
    for group in game.groups:
        group.draw(game.screen)
    
    pg.display.flip()
