"""
This module contains all the basic sprite classes in the game.
"""
import pygame as pg

from.dict_obj import DictObj


class BaseSprite(pg.sprite.Sprite):
    """
    Interface for sprites. Anything that inherits from it must 
    implement the "update()" method or else it throws errors.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__()
        self.game = game # a reference to the game the sprite is in
        self.asset_path = asset_path
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.options = options
        

    def update(self):
        raise NotImplementedError("update_function has not been overriden.")


class Backdrop(BaseSprite):
    """
    Simple sprite that does not interact but does move with the camera.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)
        self.collision_mask = pg.mask.from_surface(self.image)
    
    def update(self):
        pass


class Decal(BaseSprite):
    """
    Simple Sprite that does not move on screen.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)
    
    def update(self):
        pass


class Bedrock(Backdrop):
    """
    Sprite that is solid and cannot be walked through but otherwise
    does not interact.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)
    
    def update(self):
        pass


class Trigger(Backdrop):
    """
    Sprite that can be walked through but triggers an interaction.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)
    
    def update(self):
        pass


class Character(Trigger):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)
    
    def update(self):
        pass

SPRITE_MAP = DictObj(**{
    "BaseSprite" : BaseSprite,
    "Backdrop"   : Backdrop,
    "Decal"      : Decal,
    "Bedrock"    : Bedrock,
    "Trigger"    : Trigger,
    "Character"  : Character
})
