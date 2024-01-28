import operator
import itertools

import pygame as pg

from .decal import Decal

DEFAULT_ANIMATION = 'stand'
# NULL_PATH = "./assets/dummy/null.png"
NULL_PATH = "./assets/dummy/block.png"

class Animation():
    def __init__(self, sprite, **options):
        
        self.sprite = sprite
        self.data = {}
        self.current = None # the current animation
        self.previous = None # the id of the previous animation
        self.frame = None # next frame generator
        self.frame_times = [1] # list of frame times
        self.frame_time = 1 # the number of ms the current frame should show
        self.last_frame_time = 0 # the previous frame time
        self.active = False # is the animation active?
        self.last_direction = self.sprite.direction

        for animation in options['animations']:
            key_frame_size = [
                int(x) for x in animation['key_frame_size'].split(',')
            ]
            animation['frames'] = self.parse_animation(
                animation['asset_path'], key_frame_size
            )
            # add a special mask if it exists
            if 'mask_path' in animation:
                animation['mask'] = self.parse_animation(
                    animation['mask_path'], key_frame_size,
                    make_mask=True
                )
            self.data[animation['id']] =  animation
             
        self.current = self.data[DEFAULT_ANIMATION]
        self.null_image = self.data['null']['frames'][0][0]
        self.alt_sprite = Decal(**{
                "id": self.sprite.id + "_alt",
                "scene": self.sprite.scene,
                "asset_path": NULL_PATH,
            })
        self.alt_sprite.rect.center = (500, 500)



    def kill(self):
        self.alt_sprite.kill()
        
    def parse_animation(self, asset_path, frame_size, make_mask=False): 
        main_image = pg.image.load(asset_path).convert_alpha()
        main_size = main_image.get_size()
        nframesx, nframesy = map(operator.floordiv, main_size, frame_size)
        kf_w, kf_h = frame_size
        # construct a frame group (matrix of sub-images)
        frame_group = [[main_image.subsurface([kf_w * i, kf_h * j, kf_w, kf_h]) 
                for i in range(nframesx)
            ] for j in range(nframesy)
        ]
        # turn them into masks if applicable
        if make_mask:
            frame_group = [list(map(pg.mask.from_surface, group))
                for group in frame_group
            ]

        return frame_group


    def animate(self):
        set_frame = False
        # update animation if changed
        if self.current['id'] != self.previous:
            set_frame = True
            self.previous = self.current['id']
            self.frames = self.current["frames"][self.sprite.direction]

        # update direction if it has changed
        if self.sprite.direction != self.last_direction:
            set_frame = True
            self.last_direction = self.sprite.direction
            self.frames = self.current["frames"][self.sprite.direction]
        
        if set_frame: self.set_frame()

        # if enough time has passed, set the new image
        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.set_image(next(self.frame, None))
            self.frame_time = next(self.frame_times)
            self.last_frame_time = cur_time
            if 'mask' in self.current.keys():
                self.alt_sprite.mask = next(self.alt_sprite.mask_set)
        
        if self.sprite.image is None: # animation is done
            self.active = False
            last_animate = self.previous
            self.previous = self.current['id']
            self.current = self.data[last_animate]
            self.set_frame()


    def set_image(self, image):
        if self.sprite.image == self.null_image:
            self.alt_sprite.image = self.null_image
            self.alt_sprite.kill()
        self.sprite.image = image
        if image is None: return
        if self.sprite.rect.size == image.get_rect().size: return
        # set image to blank
        # then just paste the new image on top of it
        self.sprite.image = self.null_image
        for group in self.sprite.groups():
            group.add(self.alt_sprite)
        self.alt_sprite.image = image
        self.alt_sprite.rect = self.alt_sprite.image.get_rect()
        self.alt_sprite.rect.center = self.sprite.rect.center
        

    def set_frame(self):
        self.frame = (
            itertools.cycle(self.frames) 
            if self.current['repeat']
            else iter(self.frames)
        )
        self.frame_times = itertools.cycle(self.current['key_frame_times'])
        self.set_image(next(self.frame, None))
        self.frame_time = next(self.frame_times)
        
        if 'mask' in self.current.keys():
            self.alt_sprite.mask_set = itertools.cycle(
                self.current['mask'][self.sprite.direction]
            )
            self.alt_sprite.mask = next(self.alt_sprite.mask_set)

