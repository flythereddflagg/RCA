"""
This module contains all the basic sprite classes in the game.
"""
from dataclasses import dataclass

import yaml
import pygame as pg

from .dict_obj import DictObj
from .tools import load_yaml
from .animation import Animation
from .node import Node


@dataclass
class Original:
    image:pg.surface.Surface
    mask:pg.mask.Mask
    size:tuple


class Decal(pg.sprite.Sprite):
    def __init__(
                self, 
                scene,
                image:str,
                scale:float=1, 
                mask:str=None, 
                parent:Node=None,
                animation:Animation=None,
                **kwargs
    ):
        super().__init__()
        id_ = kwargs.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self)) 
        self.image_path = image
        self.mask_path = mask
        self.init_scale = scale
        self.parent = parent
        self.animation = animation
        self.scene = scene

        self.image = pg.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = self.get_mask(mask)
        self.scale = 1.0
        self.init_scale = scale

        self.original = Original(self.image, self.mask, self.rect.size)
        self.options = kwargs
        self.scale_by(scale)


    def get_mask(self, mask_path=None) -> pg.mask.Mask:
        if mask_path is None:
            return vars(self).get('mask')

        tmp_image = (
            self.image 
            if mask_path == 'image' else 
            pg.image.load(mask_path).convert_alpha()
        )
        return pg.mask.from_surface(tmp_image)


    def scale_by(self, factor):
        self.scale *= factor
        if self.scale == 0: self.scale = 1 # 0 resets scale
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original.size]
        self.image = pg.transform.scale(self.original.image, new_size)
        # TODO see if we can change the scaling method for smoother scaling
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if self.mask:
            self.mask = self.original.mask.scale(new_size)
        if self.animation: self.animation.load_animations()


    def scale_abs(self, scale):
        self.scale_by(0)
        self.scale_by(scale)


    def update(self):
        if self.parent: self.parent.update()

    def signal(self, *args, **kwargs):
        if self.parent: self.parent.signal(*args, **kwargs)
