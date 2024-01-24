"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from .dict_obj import DictObj
from .compass import Compass
from .animation import Animation


DEFAULT_ANIMATION = 'stand'
NULL_PATH = "./assets/dummy/null.png"



class Decal(pg.sprite.Sprite):
    """
    Simple Sprite that accepts basic input.
    Backgrounds and other non-interacting sprites
    should use this class. Has an absolute initial reference.
    Moves with the camera.
    """
    requirements = [
        "id",
        "game",
        "asset_path",
        "startx",
        "starty",
    ]
    def __init__(self, **options):
        assert all([key in options for key in self.requirements]), \
            f"class must be instatiated with all of:\n {self.requirements}"
        super().__init__()
        self.id = options['id']
        self.asset_path = options["asset_path"]
        self.scene = options["game"] # a reference to the game the sprite is in
        if self.asset_path.endswith(".yaml"):
            options = {**options, 
                **self.scene.game.load_yaml(self.asset_path)
            }
        self.asset_path = options["asset_path"]
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image
        self.original_size = self.rect.size
        self.mask = None
        self.startx = options["startx"]
        self.starty = options["starty"]
        self.options = options # make this a dictobj

        # process any optional params
        if "scale" not in self.options.keys():
            self.options["scale"] = 1
        self.scale = 1
        self.set_scale(self.options["scale"])


    def set_scale(self, factor):
        self.scale *= factor
        if self.scale < 1: self.scale = 1
        pos = self.rect.center
        new_size = [dim * self.scale for dim in self.original_size]
        self.image = pg.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    
    def __repr__(self):
        string = super().__repr__()
        string += f"\n{type(self)}"
        for key, item in self.__dict__.items():
            if type(item) in [dict, DictObj]: 
                string += f"\n{str(key):10.10}: {{...}}"
                continue
            string += f"\n{str(key):10.10}: {str(item):30.30}"
        return string



class Block(Decal):
    """
    Same as Decal and initalizes its position to anchor 
    itself to the background.
    """
    def __init__(self, **options):
        super().__init__(**options)
        self.mask = pg.mask.from_surface(self.image)
        background = self.scene.layers['background'].sprites()[0]  
        self.rect.x = background.rect.x + self.startx
        self.rect.y = background.rect.y + self.starty



class Character(Block):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera. Also can be animated.
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.direction = Compass.DOWN
        self.dist_buffer = 0
        self.animation = None
        self.alt_image = None
        if 'animations' in self.options.keys():
            self.animation = Animation(self, **self.options)
            self.alt_image = Decal(**{
                "id": self.id + "_alt",
                "game": self.scene,
                "asset_path": NULL_PATH,
                "startx":0,
                "starty":0,
            })


    def move(
        self, direction:int|str|tuple, 
        distance:int=0, speed:int|float=0,
        reject_foreground:bool=True
    ) -> None:
        """
        move the character in a direction with
        move rejection from colliding with the foreground
        if speed is given it will override distance
        @param direction MUST be of type: int, str, or tuple
        @param distance MUST be of type: int
        @param speed may be int or float
        """
        if isinstance(direction, str) or isinstance(direction, tuple):
            direction = Compass.i_map[direction] # convert to int
        self.direction = direction
        if speed:
            fps = self.scene.game.clock.get_fps()
            if not fps: return
            distance = speed / fps
        if distance < 0:
            direction = Compass.opposite[direction]
            distance *= -1
        # this chunk is to correct for crazy frame rates
        self.dist_buffer += distance % 1
        distance -= distance % 1
            
        if self.dist_buffer > 1: # reset the buffer once it exceeds 1
            distance += self.dist_buffer
            self.dist_buffer = distance % 1

        distance = int(distance)
        xunit, yunit = Compass.vec_map[direction]
        addx, addy = distance * xunit, distance * yunit
        self.rect.move_ip(addx, addy)
        
        if reject_foreground: self.foreground_rejection(xunit, yunit)


    def foreground_rejection(self, xunit, yunit):
        # move rejection for foreground
        while pg.sprite.spritecollide(
            # collide between character and foreground
            self, self.scene.layers['foreground'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        ):
            self.rect.move_ip(-xunit, -yunit) # move back 1


    def kill(self):
        self.alt_image.kill()
        super().kill()
    


SPRITE_MAP = DictObj(**{
    "Decal"      : Decal,
    "Block"      : Block,
    "Character"  : Character
})
