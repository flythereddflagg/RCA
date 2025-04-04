"""
This module contains all the basic sprite classes in the game.
"""
from dataclasses import dataclass

import yaml
import pygame as pg

from .dict_obj import DictObj
from .tools import load_yaml
from .node import Node
from .animation import Animation

@dataclass
class Original:
    image:pg.surface.Surface
    mask:pg.mask.Mask
    size:tuple


class Decal(pg.sprite.Sprite):
    def __init__(
                self, 
                scene,
                image:str=None,
                scale:float=1, 
                mask:str=None, 
                parent:Node=None,
                animation:Animation=None,
                **options
    ):
        super().__init__()
        id_ = options.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self)) 
        self.options = options
        self.image_path = image
        self.mask_path = mask if mask else self.image_path
        self.init_scale = scale
        self.parent = parent
        self.scene = scene
        self.init_scale = scale
        self.image = None
        self.rect = None
        self.mask = None
        self.animation = None
        self.original = Original(None, None, None)
        self.scale = 1.0
        image = (
            pg.image.load(self.image_path).convert_alpha() 
            if self.image_path else None
        )
        mask = (
            pg.mask.from_surface(pg.image.load(self.mask_path).convert_alpha())
            if self.mask_path
            else None
        )
        
        self.set_image(image, mask)



    def scale_by(self, factor):
        self.scale *= factor
        if self.scale == 0: self.scale = 1 # 0 resets scale
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original.size]
        self.image = pg.transform.scale(self.original.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if self.mask:
            new_size = [dim * self.scale for dim in self.original.mask.get_size()]
            self.mask = self.original.mask.scale(new_size)


    def scale_abs(self, scale):
        self.scale_by(0)
        self.scale_by(scale)


    def update(self):
        if self.parent: self.parent.update()

    def signal(self, *args, **options):
        if self.parent: self.parent.signal(*args, **options)
    
    def set_image(
        self, image:pg.surface.Surface=None, mask:pg.mask.Mask=None
    ) -> None:
        cur_pos = self.rect.center if self.rect else None
        self.image = (
            image 
            if image else 
            pg.surface.Surface((32, 32), flags=pg.SRCALPHA)
        )
        self.rect = self.image.get_rect()
        
        if not mask:
            # this recenters the mask on a different-sized image 
            # when a mask is not supplied
            if self.original.mask is None:
                self.original.mask = pg.mask.Mask(size=(32, 32), fill=False)
            offset = (
                pg.math.Vector2(self.rect.center) - 
                pg.math.Vector2(self.original.mask.get_rect().center)
            )
            mask_surf = pg.Surface(self.rect.size,flags=pg.SRCALPHA)
            mask_surf.fill((0,0,0,0)) # blank the surface
            self.original.mask.to_surface(
                surface=mask_surf, unsetcolor=None, dest=offset
            )
            self.mask = pg.mask.from_surface(mask_surf)
        else:
            self.mask = mask

        self.original = Original(self.image, self.mask, self.rect.size)
        self.scale_by(self.init_scale)
        
        if cur_pos: self.rect.center = cur_pos
