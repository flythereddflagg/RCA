"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from .dict_obj import DictObj
from .tools import load_yaml


class Decal(pg.sprite.Sprite):
    def __init__(self, scene, image_path, 
        scale=1, mask_path=None, animation=None **kwargs
    ):
        super().__init__()
        # NOTE we may need to keep track of these
        self.image_path = image_path
        self.mask_path = mask_path
        self.init_scale = scale

        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.mask = self.get_mask(mask_path)
        self.animation = None if not animation else Animation(animation)
        self.scene = scene
        self.scale = 1.0

        self.original = {
            'image': self.image,
            'mask' : self.mask,
            'size' : self.rect.size
        }
        self.options = kwargs
        self.scale_by(scale)


    def get_mask(self, mask_path=None):
        if not mask_path:
            if 'mask' in vars(self).keys(): return self.mask
            return None

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
        new_size = [dim * self.scale for dim in self.original_size]
        self.image = pg.transform.scale(self.original_image, new_size)
        # TODO see if we can change the scaling method for smoother scaling
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if self.mask:
            self.mask = self.original_mask.scale(new_size)
        if self.animation: self.animation.load_animations()


    def scale_abs(self, scale):
        self.scale_by(0)
        self.scale_by(scale)
