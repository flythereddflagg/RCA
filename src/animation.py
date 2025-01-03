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
    repeat:bool


class Animation():
    """
    A system for setting the parent sprite object's image.

    """
    def __init__(
        self, parent, animations:dict, path_prefix='./'
    ):
        self.parent = parent # parent must have a 'state' attribute
        self.previous:str = None
        self.last_state:str = None
        self.last_direction:int = self.parent.move.direction
        self.last_set_frame_time = 0 # time since the last frame was set
        self.active = False # is an animation active?
        self.frame_counter = iter([]) # generator counter for the frame index
        self.frame_index = 0 # index of the current frame
        self.frame_time = 1 # duration of the current frame
        self.path_prefix = path_prefix
        self.animations = {}
        self.load_animations(animations)


    def load_animations(self, animations) -> None:
        self.animations = {}
        for state, data in animations.items():
            datafile = data['datafile'] # TODO make 'datafile' mutable to 'hitbox' and then make it so we can have a blank animation? (See the changes in hit_mask.py)
            if not datafile.endswith(JSON): continue
            json_data = load_json(self.path_prefix + datafile)
            self.animations[state] = Reel(
                state, datafile, list(), json_data['meta'], data['repeat']
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
        state:str = self.parent.state
        direction:int = self.parent.move.direction
        current:Reel = self.animations[state]
        set_reel = False

        # update animation if changed
        if state != self.previous:
            set_reel = True
            self.last_state = self.previous
            self.previous = state
            self.active = not current.repeat

        # update direction if it has changed
        if direction != self.last_direction:
            set_reel = True
            self.last_direction = direction
        
        if set_reel: self.set_reel()

        # if not enough time has passed just return
        if pg.time.get_ticks() - self.last_set_frame_time < self.frame_time:
            return
        
        # otherwise, update the frame
        self.frame_index = next(self.frame_counter, None)
        if self.frame_index is None:
            self.active = False
            self.parent.state = self.last_state
            self.set_reel()
            return

        self.set_frame()


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
        self.set_frame()


    def set_frame(self) -> None:
        """
        set the image from the current state and direction and frame index
        """
        current:Frame = (
            self.animations[self.parent.state].frames[self.frame_index]
        )
        self.parent.sprite.set_image(current.image)
        self.frame_time = current.duration
        self.last_set_frame_time = pg.time.get_ticks()
 


