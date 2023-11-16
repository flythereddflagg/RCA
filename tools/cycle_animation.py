# This file will animate a sprite with a convention I will come up with.

# TODO write the code that will load this!
import sys
import pygame as pg
import yaml

from src.sprite import BaseSprite
from src.dict_obj import DictObj

BLACK = (0,0,0)
SCREENWIDTH, SCREENHEIGHT = 600, 600
FPS = 30

class PlayerAnimation(BaseSprite):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
    
    def update(self):
        pass




def init_game(animation_path):
    pg.init()

    # read_init_data
    # with open(data_path) as f:
    #     raw_yaml = f.read()

    # game = DictObj(**yaml.load(raw_yaml, Loader=yaml.Loader))
    game = DictObj()
    
    # set screen size
    screen = pg.display.set_mode(
        [SCREENWIDTH, SCREENHEIGHT]
    )
    game.clock = pg.time.Clock()
    game.screen = screen
    player = PlayerAnimation(game, animation_path,
        SCREENWIDTH // 2, SCREENHEIGHT // 2,
        scale=2
    )
    group = pg.sprite.Group()
    group.add(player)
    game.groups = [group]
    return game



def run_game(game):
    game.running = True

    while game.running:
        game_input = get_input(game)
        if "QUIT" in game_input: 
            game.running = False
            continue
        # game.logic(game_input)
        draw_frame(game)
        
        game.clock.tick(FPS)
    pg.display.quit()
    pg.quit()


def get_input(game):
    game_input = []

    # make the exit button work
    events = pg.event.get()
    if pg.QUIT in [event.type for event in events]: return ["QUIT"]    

    return game_input


def draw_frame(game):
    
    game.screen.fill(BLACK)
    for group in game.groups:
        group.draw(game.screen)
    
    pg.display.flip()

if __name__ == "__main__":
    data_path = sys.argv[1]
    game = init_game(data_path)
    run_game(game)

# test this with: 
# python -m tools.cycle_animation ./assets/dummy/character_walking.png
