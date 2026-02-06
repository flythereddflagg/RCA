import math

import pygame as pg

from .compass import Compass
from .tools import list_collided

BUFFER_LIMIT = 1/2

class Movement():
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera. Also can be animated.
    """

    def __init__(self, sprite, **init):
        self.sprite = sprite
        self.direction = Compass.DOWN
        self.dist_buffer:list[float] = [0.0 for _ in Compass.indicies]

    def __call__(
        self, direction:int|str|tuple|pg.math.Vector2,
        distance:float=0, speed:float=0,
        reject_foreground:bool=True, change_direction=True
    ) -> None:
        """
        move the character in a direction with
        move rejection from colliding with the foreground
        if speed is given it will override distance
        @param direction MUST be of type: int, str, or tuple 
        @param distance MUST be of type: int
        @param speed may be int or float
        """
        i_dir:int = Compass.index(direction)
        if change_direction: 
            self.direction = i_dir
        if speed:
            fps = self.sprite.scene.game.clock.get_fps()
            if not fps: return
            distance += speed / fps
        if distance < 0:
            direction = Compass.opposite(direction)
            distance *= -1
        print(distance, end=" -> ")
        # TODO CONTINUE HERE Need to cancel opposite directions
        i_distance:int = int(distance)
        buff_dist = distance % 1
        self.dist_buffer[i_dir] += buff_dist
        i_distance += int(self.dist_buffer[i_dir])
        self.dist_buffer[i_dir] -= int(self.dist_buffer[i_dir])
        
        print(i_distance)
        
        xunit, yunit = Compass.vector(direction)
        addx, addy = i_distance * xunit, i_distance * yunit
        self.sprite.rect.move_ip(addx, addy)
        
        if reject_foreground: self.foreground_rejection(xunit, yunit)


    def foreground_rejection(self, xunit, yunit):
        if not xunit and not yunit: return # protects against infinite loop
        if 'solid' not in self.sprite.scene.groups.keys(): return
        if 0 < abs(xunit) < 1: xunit = int(xunit / abs(xunit))
        if 0 < abs(yunit) < 1: yunit = int(yunit / abs(yunit))
        while list_collided(self.sprite, self.sprite.scene.groups['solid']):
            self.sprite.rect.move_ip(-xunit, -yunit) # move back 1

