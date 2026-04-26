"""
This module contains all the basic sprite classes in the game.
"""
from dataclasses import dataclass

import yaml
import pygame as pg

from .dict_obj import DictObj
from .tools import load_yaml, diff_vec
from .node import Node

@dataclass
class Original:
    image:pg.surface.Surface
    mask:pg.mask.Mask
    size:tuple


class Decal(Node):
    """
    Decal will the "Sprite" class in that
    it is guarenteed to contain 3 child objects
    namely a pg.surface.Surface (image), 
    pg.mask.Mask (mask) and a pg.Rect (rect)
    also it is guaranteed to have an update function
    from the parent class
    """

    def setup(self):
        self.sprite = self
        self.rotation = 0      

        self.image_path:str = self.init.get("image")
        self.mask_path:str = self.init.get("mask")
        self.init_scale:float = self.init.get("scale", 1)

        self.image = (
            pg.image.load(self.image_path).convert_alpha() 
            if self.image_path 
            else self.get_null(mask=False)
        )
        self.rect = self.image.get_rect()
        self.mask = (
            pg.mask.from_surface(pg.image.load(self.mask_path).convert_alpha())
            if self.mask_path
            else self.get_null(mask=True)
        )
        self.original = Original(self.image, self.mask, self.rect.size)
        self.scale = 1.0
        
        # this needs to run to initally set the scale
        self.set_image(self.image, self.mask)
        self.scale_by(self.init_scale, absolute=True)
        

    def update(self):
        # if self.parent: self.parent.update()
        pass


    def scale_by(self, factor, absolute=False):
        self.scale = factor if absolute else self.scale * factor
        assert self.scale > 0, f"{self.id}: Scale must be > 0"
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original.size]
        self.image = pg.transform.scale(self.original.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        new_mask_size = [
            dim * self.scale 
            for dim in self.original.mask.get_size()
        ]
        self.mask = self.original.mask.scale(new_mask_size)
   

    def set_image(
        self, image:pg.surface.Surface=None, mask:pg.mask.Mask=None,
    ) -> None:
        """
        Sets the image of the sprite and the mask if supplied.
        If if one is not supplied, it will not change
        If neither is supplied, this does nothing
        """
        if image:
            cur_pos = self.rect.center
            self.image = image
            self.rect = self.image.get_rect()
        
        if mask:
            self.mask = mask

        elif not mask and image:
            # this recenters the current mask
            # when there is a new image but no new mask
            offset = diff_vec(
                self.rect.center, self.original.mask.get_rect().center
            )
            mask_surf = pg.Surface(self.rect.size, flags=pg.SRCALPHA)
            mask_surf.fill((0,0,0,0)) # blank the surface
            self.original.mask.to_surface(
                surface=mask_surf, unsetcolor=None, dest=offset
            )
            self.mask = pg.mask.from_surface(mask_surf)
      
        if image:
            # update the original, rescale and place if the image has changed
            self.original = Original(self.image, self.mask, self.rect.size)
            # self.scale_by(self.scale, absolute=True)
            self.rect.center = cur_pos
        
        if self.scale != 1:
            self.scale_by(self.scale, absolute=True)
        
        if self.rotation:
            cur_pos = self.rect.center
            self.image = pg.transform.rotate(image, self.rotation)
            self.rect = self.image.get_rect()
            self.rect.center = cur_pos

    
    def get_null(self, mask:bool=False) -> pg.surface.Surface|pg.mask.Mask:
        """
        Returns an empty image or pygame surface if 'mask' is False.
        Else, it returns an empty pygame Mask
        """
        if mask:
            return pg.mask.Mask(size=(32, 32), fill=False)

        return pg.surface.Surface((32, 32), flags=pg.SRCALPHA)

    def kill(self):
        self.rect.topleft = (0,0)
        super().kill()