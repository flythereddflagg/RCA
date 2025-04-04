import pygame as pg

from .compass import Compass
from .tools import mask_collision


class Movement():
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera. Also can be animated.
    """

    def __init__(self, sprite, **options):
        self.sprite = sprite
        self.direction = Compass.DOWN
        self.dist_buffer = 0

    def __call__(
        self, direction:int|str|tuple|pg.math.Vector2,
        distance:int=0, speed:int|float=0,
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
        
        if change_direction: self.direction = Compass.index(direction)
        if speed:
            fps = self.sprite.scene.game.clock.get_fps()
            if not fps: return
            distance = speed / fps
        if distance < 0:
            direction = Compass.opposite(direction)
            distance *= -1
        # this chunk is to correct for crazy frame rates
        self.dist_buffer += distance % 1
        distance -= distance % 1
            
        if self.dist_buffer > 1: # reset the buffer once it exceeds 1
            distance += self.dist_buffer
            self.dist_buffer = distance % 1

        distance = int(distance)
        # BUG cannot use Compass.vector here because it can cause an
        # infinte loop in foreground_rejection()
        xunit, yunit = Compass.unit_vector(direction)
        addx, addy = distance * xunit, distance * yunit
        self.sprite.rect.move_ip(addx, addy)
        
        if reject_foreground: self.foreground_rejection(xunit, yunit)


    def foreground_rejection(self, xunit, yunit):
        if not xunit and not yunit: return # protects against infinite loop
        if 'solid' not in self.sprite.scene.groups.keys(): return
        while mask_collision(self.sprite, self.sprite.scene.groups['solid']):
            self.sprite.rect.move_ip(-xunit, -yunit) # move back 1

