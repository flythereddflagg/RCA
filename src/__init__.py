"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""
import pygame as pg
from .game_state import GameState

BLACK = (0, 0, 0)
SHOW_EVENTS = False


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

    # read_init_data
    init_data = GameState.load_yaml(data_path)
    # set screen size
    screen = pg.display.set_mode(
        [init_data.SCREENWIDTH, init_data.SCREENHEIGHT], pg.RESIZABLE
    )
    # intialize game
    game = GameState(**init_data)
    game.screen = screen
    game.clock = pg.time.Clock()
    game.controllers = controllers
    game.load_scene(game.INITAL_SCENE)
    
    if game.FPS_COUNTER:
        game.fps_counter = pg.font.SysFont("Sans", 22)
    return game


def get_input(game):
    game_input = []

    events = pg.event.get()
    if SHOW_EVENTS:
        for event in events:
            print(event.type, event)
    if pg.QUIT in [event.type for event in events]: return ["QUIT"]    

    # TODO make the input more sophisticated
    pressed_keys = pg.key.get_pressed()
    game_input = [
        key for key, bind in game.KEY_BIND.items()
        if pressed_keys[pg.key.key_code(bind)]
    ]
    if SHOW_EVENTS and game_input: print(game_input)
    if 'FORCE_QUIT' in game_input: return ['QUIT']
    
    return game_input


def draw_frame(game):

    game.screen.fill(BLACK)
    for group_name in game.scene.data.DRAW_LAYERS:
        game.scene.layers[group_name].draw(game.screen)

    if game.FPS_COUNTER:
        fps = str(int(game.clock.get_fps()))
        fps_sprite = game.fps_counter.render(fps, True, (255,255,255))
        game.screen.blit(fps_sprite, (10,10))
    
    pg.display.flip()


def run_game(data_path):
    game = init_game(data_path)
    game.running = True

    while game.running:
        game_input = get_input(game)
        game.logic(game_input)
        draw_frame(game)
        game.dt = (
            game.clock.tick() 
            if game.FPS < -1 else 
            game.clock.tick(game.FPS)
        )

    pg.display.quit()
    pg.quit()
