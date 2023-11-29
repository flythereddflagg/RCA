"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from.dict_obj import DictObj


class BaseSprite(pg.sprite.Sprite):
    """
    Interface for sprites. Anything that inherits from it must 
    implement the "update()" method or else it throws errors.
    """      
    def update(self):
        raise NotImplementedError("update_function has not been overriden.")


class Decal(BaseSprite):
    """
    Simple Sprite that accepts basic input.
    Backgrounds and other non-interacting sprites
    should use this class. Has an absolute initial reference.
    Moves with the camera.
    """
    requirements = [
        "game",
        "asset_path",
        "startx",
        "starty",
    ]
    def __init__(self, **options):
        assert all([key in options for key in self.requirements]), \
            f"class must be instatiated with all of:\n {self.requirements}"
        super().__init__()

        self.asset_path = options["asset_path"]
        self.game = options["game"] # a reference to the game the sprite is in
        if self.asset_path.endswith(".yaml"):
            extra_opts = self.game.load_yaml(self.asset_path)
            options = {**options, **extra_opts}
        self.asset_path = options["asset_path"]
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.startx = options["startx"]
        self.starty = options["starty"]
        self.options = options # make this a dictobj

        # process any optional params
        if "scale" not in self.options.keys():
            self.options["scale"] = 1
        self.set_scale(self.options["scale"])


    def set_scale(self, scale):
        self.scale = scale
        new_size = [dim * scale for dim in self.rect.size]
        self.image = pg.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()
        
    
    def update(self):
        pass


class Block(Decal):
    """
    Same as Decal and anchors itself to the background.
    """
    def __init__(self, **options):
        super().__init__(**options)
        self.mask = pg.mask.from_surface(self.image)
        background = self.game.groups['background'].sprites()[0]

        bg_map = {
            'center' : background.rect.center,
        }
        if self.startx in bg_map.keys():
            self.rect.x = bg_map[self.startx][0]
        else:    
            self.rect.x = background.rect.x + self.startx

        if self.starty in bg_map.keys():
            self.rect.y = bg_map[self.starty][1]
        else:
            self.rect.y = background.rect.y + self.starty


class Character(Block):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera. Also can be animated.
    """
    def move(self, direction, distance):
        xunit, yunit = direction
        addx, addy = distance * xunit, distance * yunit
        self.rect.x += addx 
        self.rect.y += addy


SPRITE_MAP = DictObj(**{
    "Decal"      : Decal,
    "Block"      : Block,
    "Character"  : Character
})
