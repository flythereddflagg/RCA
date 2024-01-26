import pygame as pg

from .decal import Decal
from .compass import Compass
from .animation import Animation


DEFAULT_ANIMATION = 'stand'
NULL_PATH = "./assets/dummy/null.png"


class Character(Decal):
    """
    Non-solid sprite that triggers interaction and moves 
    independently of the camera. Also can be animated.
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.direction = Compass.DOWN
        self.dist_buffer = 0
        self.animation = None
        if 'animations' in self.options.keys():
            self.animation = Animation(self, **self.options)

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
        self.animation.kill()
        super().kill()
    



