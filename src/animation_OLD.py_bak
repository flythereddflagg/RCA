import operator
import itertools

import pygame as pg

from .decal import Decal

DEFAULT_ANIMATION = 'stand'
NULL_PATH = "./assets/block/null.png"
# NULL_PATH = "./assets/block/block.png"

class Animation():
    def __init__(self, sprite, **options):
        
        self.sprite = sprite
        self.data = options
        self.current = None # the current animation
        self.previous = None # the id of the previous animation
        self.frame = None # next frame generator
        self.frame_times = [1] # list of frame times
        self.frame_time = 1 # the number of ms the current frame should show
        self.last_frame_time = 0 # the previous frame time
        self.active = False # is current the animation active?
        self.last_direction = self.sprite.move.direction


        self.load_animations()
        self.current = self.data[DEFAULT_ANIMATION]
        self.null_image = self.data['null']['frames'][0][0]
        self.null_mask = pg.mask.from_surface(self.null_image)
        self.alt_sprite = Decal(**{
                "id": self.sprite.id + "_alt",
                "scene": self.sprite.scene,
                "image": NULL_PATH,
                "mask" : 'image'
            })

    def load_animations(self):
        for animation in self.data['animations']:
            key_frame_size = animation['key_frame_size']
            animation['frames'] = self.parse_animation(
                animation['image'], key_frame_size, self.sprite.scale
            )
            # add a special mask if it exists
            if 'mask_path' in animation:
                animation['mask'] = self.parse_animation(
                    animation['mask_path'], key_frame_size, self.sprite.scale,
                    make_mask=True
                )
                for frames in animation['frames']:
                    assert frames, f'issue: no frames for "{animation["id"]}" {animation["frames"]}'
            self.data[animation['id']] =  animation

    def kill(self):
        self.alt_sprite.kill()
        
    def parse_animation(
        self, image_path:str, frame_size:tuple[int, int], 
        scale:float, make_mask:bool=False
    ):
        main_image = pg.image.load(image_path).convert_alpha()
        new_size = pg.math.Vector2(main_image.get_size()) * scale
        frame_size = list(map(int, pg.math.Vector2(frame_size) * scale))
        main_image = pg.transform.scale(main_image, new_size)
        main_size = main_image.get_size()
        nframesx, nframesy = map(
            int, map(operator.floordiv, main_size, frame_size)
        )
        kf_w, kf_h = frame_size
        assert all([nframesx,nframesy,kf_h,kf_w]), \
            f"invalid frame parsing {[nframesx,nframesy,kf_h,kf_w]}"
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


    def update(self):
        set_frame = False
        # update animation if changed
        if self.current['id'] != self.previous:
            set_frame = True
            self.last_animation = self.previous
            self.previous = self.current['id']
            self.frames = self.current["frames"][self.sprite.move.direction]
            self.active = not self.current["repeat"]

        # update direction if it has changed
        if self.sprite.move.direction != self.last_direction:
            set_frame = True
            self.last_direction = self.sprite.move.direction
            self.frames = self.current["frames"][self.sprite.move.direction]
        
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
            self.active = False # this stops the animation
            self.current = self.data[self.last_animation] # reset to last
            self.set_frame()


    def set_image(self, image):
        if self.sprite.image == self.null_image:
            self.alt_sprite.image = self.null_image
            self.alt_sprite.mask = self.null_mask
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
                self.current['mask'][self.sprite.move.direction]
            )
            self.alt_sprite.mask = next(self.alt_sprite.mask_set)

