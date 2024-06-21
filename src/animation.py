from dataclasses import dataclass
import pprint

import pygame as pg

from .tools import load_json

JSON = '.json'
@dataclass
class Frame:
    name:str
    image:pg.surface.Surface
    mask:pg.mask.Mask
    frame:dict
    rotated:bool
    trimmed:bool
    spriteSourceSize:dict
    sourceSize:dict
    duration:int

@dataclass
class Reel:
    name:str
    datafile:str
    frames:list[Frame]
    meta:dict
    repeat:bool=True

class Animation():
    """
    A system for setting the parent sprite object's image.

    """
    def __init__(
        self, sprite:pg.sprite.Sprite, animations:dict, path_prefix='./'
    ):
        self.sprite = sprite
        self.previous = None
        self.active = False
        self.path_prefix = path_prefix
        self.animations = {}
        self.load_animations(animations)


    def load_animations(self, animations) -> None:
        self.animations = {}
        for state, data in animations.items():
            datafile = data['datafile']
            if not datafile.endswith(JSON): continue
            json_data = load_json(self.path_prefix + datafile)
            self.animations[state] = Reel(
                state, datafile, list(), json_data['meta']
            )
            master_image = pg.image.load(
                self.path_prefix + self.animations[state].meta['image']
            ).convert_alpha()

            for name, frame in json_data['frames'].items():
                frame["name"] = name
                frame["image"] = master_image.subsurface(
                    list(frame['frame'].values())
                )
                frame["mask"] = pg.mask.from_surface(frame["image"])
                self.animations[state].frames.append(Frame(**frame))


    def update(self) -> None:
        pass


    def set_action(self, action:str) -> None:
        """Sets the current animation action and direction"""
        pass


    def cancel(self) -> None:
        """Force cancels the animation back to the previous one"""
        pass