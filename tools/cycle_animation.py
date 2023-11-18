# This file will animate a sprite with a convention I will come up with.

# TODO write the code that will load this!
import sys
import math
import pygame as pg
import yaml


from src.sprite import BaseSprite
from src.dict_obj import DictObj

BLACK = (0,0,0)
SCREENWIDTH, SCREENHEIGHT = 600, 600
FPS = 30
# order is ALWAYS up, right, down, left  

class PlayerAnimation(BaseSprite):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
        self.animation_image = self.image
        self.key_frame_size = [32, 32]
        self.n_keyframes = [
            bg // kf
            for bg, kf in zip(
                self.animation_image.get_rect().size,  self.key_frame_size
            )
        ]

        self.key_frame_groups = [
            [
                self.animation_image.subsurface(
                    [
                        self.key_frame_size[0] * i, self.key_frame_size[1] * j
                    ] + self.key_frame_size)
                for i in range(self.n_keyframes[0])
            ]
            for j in range(self.n_keyframes[1])
        ]
        self.key_frames = self.key_frame_groups[3]
        # TODO update so that keyframes are updated with input
        self.key_frame_times = [75 for i in self.key_frames]
        self.key_frame = self.gen_from_list(self.key_frames)
        self.key_frame_time = self.gen_from_list(self.key_frame_times)
        self.frame_time = next(self.key_frame_time)
        self.image = next(self.key_frame)
        self.last_frame_time = 0
    
    def gen_from_list(self, item_list):
        while True:
            for item in item_list:
                yield item
        
    def update(self):
        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.image = next(self.key_frame)
            self.frame_time = next(self.key_frame_time)
            self.last_frame_time = cur_time



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
        20,20,
        scale=10
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
