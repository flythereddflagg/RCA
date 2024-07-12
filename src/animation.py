from dataclasses import dataclass
import itertools
import pprint

import pygame as pg

from .tools import load_json
from .compass import Compass

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
        self.parent = parent # parent must have a 'state' attribute
        self.previous:str = None
        self.last_direction:int = None
        self.previous_tick_time = 0
        self.active = False
        self.frame_counter = iter([])
        self.frame_index = 0
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
        state:str = self.parent.state
        current:Reel = self.animations[state]
        set_reel = False
        # update animation if changed
        if state != self.previous:
            set_reel = True
            self.previous = state
            self.active = not current.repeat

        # update direction if it has changed
        if self.parent.move.direction != self.last_direction:
            set_reel = True
            self.last_direction = self.parent.move.direction
        
        if set_reel: self.set_reel()

        cur_time = pg.time.get_ticks()
        frame_time = current.frames[self.frame_index].duration 
        while cur_time - self.previous_tick_time > frame_time:
            self.previous_tick_time += frame_time
            self.frame_index = next(self.frame_counter, None)
            self.set_image()
            frame_time = current.frames[self.frame_index].duration


    def set_reel(self) -> None:
        """Set the generator "self.frame_counter" that 
        will produce the indices in the reel to run
        from direction and state data"""
        state:str = self.parent.state
        direction:int = self.parent.move.direction
        current:Reel = self.animations[state]
        frame_tags:list[dict] = current.meta['frameTags']
        tag = {}
        for d_tag in range(len(frame_tags)):
            if Compass.index(frame_tags[d_tag]['name'].upper()) == direction:
                tag = d_tag
                break

        else: raise Exception("I done goofed on this.")

        meta_dict = frame_tags[tag]
        counter = range(meta_dict['from'], meta_dict['to'] + 1)
        self.frame_counter = (
            itertools.cycle(counter) 
            if current.repeat
            else iter(counter)
        )
        self.frame_index = next(self.frame_counter, None)
        self.set_image()

    def set_image(self):
        """
        set the image from the current state and direction and frame index
        """
        current:Reel = self.animations[self.parent.state]
        cur_pos = self.parent.sprite.rect.center
        self.parent.sprite.image = current.frames[self.frame_index].image
        self.parent.sprite.rect = self.parent.sprite.image.get_rect()
        self.parent.sprite.rect.center = cur_pos
        self.parent.sprite.mask = self.parent.sprite.get_mask('image')

