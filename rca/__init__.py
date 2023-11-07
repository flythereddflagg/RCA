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


    return game


def run_game(game):
    game.running = True
    game_clock = pg.time.Clock()

    while game.running:
        game_input = get_input(game)
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
    for event in events:
        print(event.type, event)

    # get keyboard keys
    game_input = [
        i 
        for i, pressed in enumerate(pg.key.get_pressed()) 
        if pressed
    ]
    if game_input: print(game_input)

    return game_input


def draw_frame(game):
    
    game.screen.fill(BLACK)
    for group in game.groups:
        group.draw(game.screen)
    
    pg.display.flip()
