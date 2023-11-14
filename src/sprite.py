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
    def __init__(self, game, asset_path, startx, starty, scale=None, **options):
        super().__init__()
        self.game = game # a reference to the game the sprite is in
        self.asset_path = asset_path
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        if scale is not None:
            new_size = [dim * scale for dim in self.rect.size]
            self.image = pg.transform.scale(self.image, new_size)
            self.rect = self.image.get_rect()
            
        self.options = options
        if not type(startx) is str:
            self.rect.x = startx
        if not type(starty) is str:
            self.rect.y = starty
        

    def update(self):
        raise NotImplementedError("update_function has not been overriden.")


class Backdrop(BaseSprite):
    """
    Simple sprite that does not interact but does move with the camera.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)

    
    def update(self):
        pass


class Decal(BaseSprite):
    """
    Simple Sprite that does not move on screen.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
    
    def update(self):
        pass


class Bedrock(Backdrop):
    """
    Sprite that is solid and cannot be walked through but otherwise
    does not interact.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
        self.collision_mask = pg.mask.from_surface(self.image)
        background = self.game.groups[
            self.game.group_enum['background']
        ].sprites()[0]

        bg_map = {
            'center' : background.rect.center,
        }
        if startx in bg_map.keys():
            self.rect.x = bg_map[startx][0]
        else:    
            self.rect.x += background.rect.x
        if starty in bg_map.keys():
            self.rect.y = bg_map[startx][1]
        else:
            self.rect.y += background.rect.y
    
    def update(self):
        pass


class Trigger(Bedrock):
    """
    Sprite that can be walked through but triggers an interaction.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
    
    def update(self):
        pass


class Character(Trigger):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera.
    """
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)
    
    def update(self):
        pass

    def move(self, direction, distance):
        xunit, yunit = direction
        addx, addy = distance * xunit, distance * yunit
        self.rect.x += addx 
        self.rect.y += addy


SPRITE_MAP = DictObj(**{
    "BaseSprite" : BaseSprite,
    "Backdrop"   : Backdrop,
    "Decal"      : Decal,
    "Bedrock"    : Bedrock,
    "Trigger"    : Trigger,
    "Character"  : Character
})
