"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from .dict_obj import DictObj
from .tools import load_yaml


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
        "image",
        "mask"
    ]
    def __init__(self, **options):
        if 'yaml' in options.keys():
            options = {
                **options, **load_yaml(options['yaml'])
            }
        assert all([key in options for key in self.requirements]), \
            f"class {options['id']} must be instatiated with all "\
            f"of:\n {self.requirements}\ngot: {list(options.keys())}"
        super().__init__()
        self.id = options['id']
        self.scene = options["scene"]
        self.image = pg.image.load(options["image"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = None
        mask_path = (
            options[options['mask']] 
            if options['mask'] in options.keys() else 
            options['mask']
        )
        if mask_path is not None:
            self.mask = pg.mask.from_surface(
                pg.image.load(mask_path).convert_alpha()
            )
        self.original_image = self.image
        self.original_size = self.rect.size
        self.options = options

        # process any optional params
        self.animation = None
        self.scale = 1
        if "scale" in self.options.keys():
            self.set_scale(self.options["scale"])
        if 'start' in options.keys():
            background = self.scene.layers['background'].sprites()[0]
            self.start = [int(d) for d in options['start'].split(',')]
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
        if self.mask:
            self.mask = self.mask.scale(new_size)
            # FIXME there is an issue with how the mask is reloaded.
            # RELOAD MASK FROM ORIGINAL???
        if self.animation: self.animation.load_animations()
    
    
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
