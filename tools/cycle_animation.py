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

def gen_image(image_list):
    while True:
        for image in image_list:
            yield image
    

class PlayerAnimation(BaseSprite):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
        self.animation_image = self.image
        animation_image_size_y = self.animation_image.get_rect().size[1]
        self.key_frame_size = [animation_image_size_y, animation_image_size_y]
        self.n_keyframes = self.animation_image.get_rect().size[0] // \
            animation_image_size_y
        self.key_frames = [
            self.animation_image.subsurface(
                [
                    animation_image_size_y * i, 0
                ] + self.key_frame_size)
            for i in range(self.n_keyframes)
        ]
        self.key_frame = gen_image(self.key_frames)
        
    
    def update(self):
        self.image = next(self.key_frame)




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
