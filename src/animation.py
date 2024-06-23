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
        self, parent, animations:dict, path_prefix='./'
    ):
        self.parent = parent
        self.previous = None
        self.last_direction = None
        self.last_frame_time = 0
        self.active = False
        self.frame_counter = iter()
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
        # FIXME is currently in non-working state
        state = self.parent.state
        current = self.animations[state]
        set_frame = False
        # update animation if changed
        if state != self.previous:
            set_frame = True


        # update direction if it has changed
        if self.sprite.move.direction != self.last_direction:
            set_frame = True
            self.last_direction = self.sprite.move.direction
            self.frames = self.current["frames"][self.sprite.move.direction]
        
        if set_frame: self.set_frame()
        cur_time = pg.time.get_ticks()
        if cur_time - self.last_frame_time > - 0:
            self.set_image()

