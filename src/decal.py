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
    """
    Every decal is guaranteed to have an image, mask, and rect
    even if the image an mask are blank.
    """
    def __init__(
                self, 
                scene,
                image:str=None,
                mask:str=None,
                scale:float=1.0, 
                parent:Node=None,
                animation:Animation=None,
                **options
    ):
        super().__init__()
        self.sprite = self
        id_ = options.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.scene = scene
        self.scale = 1.0
        
        self.image_path = image
        self.mask_path = mask
        self.init_scale = scale
        self.parent = parent
        self.animation = None
        self.options = options
        
        proto_image = (
            pg.image.load(self.image_path).convert_alpha() 
            if self.image_path 
            else pg.surface.Surface((32, 32), flags=pg.SRCALPHA)
        )
        proto_mask = (
            pg.mask.from_surface(pg.image.load(self.mask_path).convert_alpha())
            if self.mask_path
            else pg.mask.Mask(size=(32, 32), fill=False)
        )
        self.rect = proto_image.get_rect()

        self.set_image(proto_image, proto_mask)


    def update(self):
        if self.parent: self.parent.update()


    def scale_by(self, factor):
        self.scale *= factor
        if self.scale == 0: self.scale = 1 # 0 resets scale
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original.size]
        self.image = pg.transform.scale(self.original.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if self.mask:
            new_size = [
                dim * self.scale 
                for dim in self.original.mask.get_size()
            ]
            self.mask = self.original.mask.scale(new_size)


    def scale_abs(self, scale):
        self.scale_by(0)
        self.scale_by(scale)


    def signal(self, *args, **options):
        if self.parent: self.parent.signal(*args, **options)
    
    def set_image(
        self, image:pg.surface.Surface=None, mask:pg.mask.Mask=None
    ) -> None:
        """
        For the current Decal:
            - if image is supplied, set the image of the sprite
            - if the maks is supplied, set the new mask
        If either one are not included (i.e. default to None),
        keep the previous image/mask.
        If the image changes in size compared to the old image, 
        center the mask on the new image
        """
        cur_pos = self.rect.center if self.rect else None
        self.image = image
        self.rect = self.image.get_rect()
        
        if not mask:
            # this recenters the mask on a different-sized image 
            # when a mask is not supplied
            offset = (
                pg.math.Vector2(self.rect.center) - 
                pg.math.Vector2(self.mask.get_rect().center)
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
