from dataclasses import dataclass
import itertools

import pygame as pg

from .tools import load_json
from .compass import Compass
from .node import Node
from .decal import Decal

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
    frames:list[int]
    meta:dict
    repeat:bool


class Animation2(Node):
    """
    A system for setting the parent sprite object's image.
    """
    def setup(self):
        self.require_attr("datafile")
        self.previous:str = None
        self.last_state:str = None
        self.last_direction:int = Compass.DOWN 
        self.last_set_frame_time = 0 # time since the last frame was set
        self.active = False # is an animation active?
        self.frame_counter = iter([]) # generator counter for the frame index
        self.frame_index = 0 # index of the current frame
        self.frame_time = 1 # duration of the current frame
        self.path_prefix = self.init.get('path_prefix', "./")
        # TODO -4- evaluate if we need strict mode?
        self.strict = self.init.get("strict", True) # set keyerror on fail
        self.sequence = iter(self.init.get("sequence", []))
        self.load_animation()


    def load_animation(self) -> None:
        self.animation = {}
        filename = self.init["datafile"]
        json_data = load_json(self.path_prefix + filename)
        meta = json_data['meta']
        frames = json_data["frames"]
        master_image = pg.image.load(
            self.path_prefix + meta['image']
        ).convert_alpha()
        for frametag in meta["frameTags"]:
            state = frametag['name']
            # repeat gets stored as string when you specify it
            # so if you see repeat is a string we will assume
            # it does not repeat
            repeat = frametag.get("repeat", True)
            if isinstance(repeat, str):
                repeat = False
            self.animation[state] = Reel(
                name=state,
                frames=[frametag["from"], frametag["to"] + 1],
                meta=frametag,
                repeat=repeat
            )
        self.all_frames = []
        for name, frame in frames.items():
                frame["name"] = name
                frame["image"] = master_image.subsurface(
                    list(frame['frame'].values())
                )
                frame["mask"] = pg.mask.from_surface(frame["image"])
                self.all_frames.append(Frame(**frame))


    def update(self) -> None:
        state:str = self.parent.state
        direction:int = (
            self.parent.move.direction 
            if hasattr(self.parent, "move") else
            0
        )
        # TODO -4- evaluate if we need strict mode?
        if self.strict:
            current:Reel = self.animation[state]
        else:
            current:Reel = self.animation.get(state, self.previous)
            
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
            # self.parent.state = self.last_state
            self.parent.state = self.default_state
            self.set_reel()
            return

        self.set_frame()


    def set_reel(self) -> None:
        """Set the generator "self.frame_counter" that 
        will produce the indices in the reel to run
        from direction and state data"""
        state:str = self.parent.state
        # TODO -4- evaluate if we need strict mode?
        if self.strict:
            current:Reel = self.animation[state]
        else:
            current:Reel = self.animation.get(state, self.previous)
        
        counter = range(*current.frames)
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
            self.all_frames[self.frame_index]
        )
        self.parent.sprite.set_image(current.image)
        self.frame_time = current.duration
        self.last_set_frame_time = pg.time.get_ticks()


    def get_blank_reel(self, state:str) -> Reel:
        return Reel(
            name=state,
            frames=[0],
            meta=dict(),
            repeat=True
        )
    
    
    def advance(self, end=None):
        next_state = next(self.sequence, None)
        if next_state is None:
            return end
        else:
            self.parent.state = next_state
            return next_state
