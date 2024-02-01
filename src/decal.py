"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from .dict_obj import DictObj


class Decal(pg.sprite.Sprite):
    """
    Simple Sprite that accepts basic input.
    Backgrounds and other non-interacting sprites
    should use this class. Has an absolute initial reference.
    Moves with the camera.
    """
    requirements = [
        "id",
        "scene",
        "asset_path"
    ]
    def __init__(self, **options):
        assert all([key in options for key in self.requirements]), \
            f"class must be instatiated with all of:\n {self.requirements}"\
            f"\ngot: {list(options.keys())}"
        super().__init__()
        self.id = options['id']
        self.scene = options["scene"]
        if options["asset_path"].endswith(".yaml"):
            options = {**options, 
                **self.scene.game.load_yaml(options["asset_path"])
            }
        self.asset_path = options["asset_path"]
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image
        self.original_size = self.rect.size
        self.options = options # make this a dictobj

        # process any optional params
        if "scale" not in self.options.keys():
            self.options["scale"] = 1
        self.scale = 1
        self.set_scale(self.options["scale"])
        if 'start' in options.keys():
            self.start = [int(d) for d in options['start'].split(',')]
            self.mask = pg.mask.from_surface(self.image)

            background = self.scene.layers['background'].sprites()[0]
            self.rect.topleft = (
                pg.math.Vector2(background.rect.topleft) + 
                pg.math.Vector2(self.start)
            )


    def set_scale(self, factor):
        self.scale *= factor
        if self.scale < 1: self.scale = 1
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original_size]
        self.image = pg.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    
    def __repr__(self):
        string = super().__repr__()
        string += f"\n{type(self)}"
        for key, item in vars(self).items():
            if type(item) in [dict, DictObj]: 
                string += f"\n{str(key):10.10}: {{...}}"
                continue
            string += f"\n{str(key):10.10}: {str(item):30.30}"
        return string

    def signal(self, *args, **kwargs):
        pass
