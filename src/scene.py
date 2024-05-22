import pygame as pg

from .tools import load_yaml, class_from_str
from .camera import Camera


class Scene():  
    def __init__(self, game, yaml_path, player=None):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.data = load_yaml(yaml_path)
        self.all_sprites = pg.sprite.Group()
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.SPRITE_GROUPS
        }
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.DRAW_LAYERS
        }
        for key, item in self.data.items():
            print(f"{key:20} : {item}")


    def update(self):
        pass
