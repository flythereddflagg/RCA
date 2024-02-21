# This file will animate a sprite

import sys
import math
import pygame as pg
import yaml

from src.sprite import Decal
from src.compass import Compass
from src.animation import Animation

BLACK = (255,255,255)
SCREENWIDTH, SCREENHEIGHT = 600, 600
FPS = 30
# order is ALWAYS up, right, down, left or 0, 1, 2, 3
UP, RIGHT, DOWN, LEFT = (i for i in range(4))
CONSTANT_KEY_TIME = 75
ANIMATION_BUTTON = "BUTTON_1"
ANIMATION_SELECTION = "sword swing"
DIRECTION_SELECTION = UP

UNIT_VECTORS = {
    "UP": (0,1),
    "RIGHT": (1,0),
    "DOWN": (0,-1),
    "LEFT": (-1,0),
}
DIST_PER_FRAME = 0

class PlayerAnimation(Player):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, **options):
        super().__init__(**options)
        self.animate_data = self.animation[ANIMATION_SELECTION]
        self.direction = DIRECTION_SELECTION
        
    def update(self):
        self.add_todo(ANIMATION_BUTTON)
        super().update()



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
    game.groups = []
    game.UNIT_VECTORS = UNIT_VECTORS
    game.dist_per_frame = DIST_PER_FRAME
    game.IND_UNIT_VECTORS = {
            d: i for i, d in enumerate(game.UNIT_VECTORS.keys())
        }
    game.group_enum = { "background": 0, "foreground": 1, 'player': 2}
    bg = Decal(game=game, image="./assets/dummy/null.png",
        startx=0,starty=0)
    group = pg.sprite.Group()
    group.add(bg)
    game.groups.append(group)
    game.groups.append(pg.sprite.Group()) # foreground
    player = PlayerAnimation(
        game=game, image=animation_path,
        startx=20,starty=20,
        scale=10
    )
    group = pg.sprite.Group()
    group.add(player)
    game.groups.append(group)
        
    return game



def run_game(game):
    game.running = True

    while game.running:
        game_input = get_input(game)
        if "QUIT" in game_input: 
            game.running = False
            continue
        # animation loop logic
        for group in game.groups:
            group.update()

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
# FIXME: this script is broken.