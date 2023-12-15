"""
This module contains all the basic sprite classes in the game.
"""
import yaml
import pygame as pg

from .dict_obj import DictObj
from .compass import Compass


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
        background = self.game.layers['background'].sprites()[0]

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
    required_animation_keys = [
        'asset_path', 'key_frame_size'
    ]
    def __init__(self, **options):
        super().__init__(**options)
        self.last_animate = None
        self.key_frame_group = None
        self.animate_data = None
        self.last_direction = None
        self.key_frame = None
        self.animation_active = False
        self.frame_time = 1
        self.last_frame_time = 0
        self.direction = Compass.DOWN
        self.last_direction = self.direction
        self.dist_buffer = 0
        
        # init animations
        self.key_frame_groups = {}
        self.animation = {}
        self.default_image = self.image
        self.alt_image = Decal(**{
            "id": self.id + "_alt",
            "game": self.game,
            "asset_path": NULL_PATH,
            "startx":0,
            "starty":0,
        })

        for animation in self.options['animations']:
            # load in each animation for a character 
            # defined in their yaml data
            animation['key_frames'] = self.parse_animation(
                animation['asset_path'], animation['key_frame_size']
            )
            # add a special mask if it exists
            if 'mask_path' in animation:
                animation['mask'] = self.parse_animation(
                    animation['mask_path'], animation['key_frame_size'],
                    make_mask=True
                )
            self.animation[animation['id']] =  animation


             
        self.animate_data = self.animation[DEFAULT_ANIMATION]
        self.null_image = self.animation['null']['key_frames'][0][0]


    def update(self):
        pass
        # self.animate()


    def parse_animation(self, asset_path, key_frame_size, make_mask=False): 
        animation_image = pg.image.load(asset_path).convert_alpha()
        new_size = [
            dim * self.scale 
            for dim in animation_image.get_rect().size
        ]
        animation_image = pg.transform.scale(animation_image, new_size)
        # get the size of each animation frame
        kf_sizex, kf_sizey = [
            i * self.scale for i in key_frame_size
        ]
        # calclulate the number of frames in the image
        n_keyframesx, n_keyframesy = [
            bg // kf for bg, kf in zip(
                animation_image.get_rect().size, [kf_sizex, kf_sizey]
            )
        ]
        # construct a frame group (matrix of sub-images)
        key_frame_group = [[
                animation_image.subsurface(
                    [kf_sizex * i, kf_sizey * j, kf_sizex, kf_sizey]
                ) for i in range(n_keyframesx)
            ] for j in range(n_keyframesy)
        ]
        if len(key_frame_group) == 1:
            # single frame edge case: give it 4 frames
            key_frame_group = [
                key_frame_group[0] for _ in Compass.indicies
            ]
        for direction in key_frame_group:
            for item in direction:
                assert isinstance(item, pg.Surface), f"{item} is not surface"
        if make_mask:
            key_frame_group = [
                map(
                    lambda frame: pg.mask.from_surface(frame),
                    group
                )
                for group in key_frame_group
            ]

        return key_frame_group


    def animate(self):
        set_key_frame = False
        # update animation if changed
        if self.animate_data['id'] != self.last_animate:
            set_key_frame = True
            self.last_animate = self.animate_data['id']
            self.key_frames = self.animate_data["key_frames"][self.direction]
            self.key_frame_times = self.animate_data['key_frame_times']

        # update direction if it has changed
        if self.direction != self.last_direction:
            set_key_frame = True
            self.last_direction = self.direction
            self.key_frames = self.animate_data["key_frames"][self.direction]
        
        if set_key_frame: self.set_key_frame()

        # if enough time has passed, set the new image
        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.set_image(next(self.key_frame, None))
            self.frame_time = next(self.key_frame_time)
            self.last_frame_time = cur_time
        
        if self.image is None: # animation is done
            self.animation_active = False
            last_animate = self.last_animate
            self.last_animate = self.animate_data['id']
            self.animate_data = self.animation[last_animate]
            self.set_key_frame()


    def set_image(self, image):
        if self.image == self.null_image:
            self.alt_image.image = self.null_image
        self.image = image
        if image is None: return
        if self.rect.size == image.get_rect().size: return
        # set image to blank
        # then just paste the new image on top of it
        self.image = self.null_image
        self.alt_image.image = image
        self.alt_image.rect = self.alt_image.image.get_rect()
        self.alt_image.rect.center = self.rect.center
        


    def set_key_frame(self):
        self.key_frame = self.gen_from_list(
            self.key_frames, repeat=self.animate_data['repeat']
        )
        # TODO: set up mask changes here!
        self.key_frame_time = self.gen_from_list(self.key_frame_times)
        self.set_image(next(self.key_frame, None))
        self.frame_time = next(self.key_frame_time)


    def gen_from_list(self, item_list, repeat=True):
        """
        generator for images. Repeats forever unless told otherwise.
        """
        while True:
            for item in item_list:
                yield item
            if not repeat: break


    def move(self, direction, distance):
        """
        move the character in a direction with
        move rejection from colliding with the foreground
        """
        # this chunk is to correct for crazy frame rates
        if distance < 1: # build up a buffer for high frame rates
            self.dist_buffer += distance
            distance = 0
            
        if self.dist_buffer > 1: # reset the buffer once it exceeds 1
            distance += self.dist_buffer
            self.dist_buffer = 0

        distance = int(distance)
        xunit, yunit = direction
        addx, addy = distance * xunit, distance * yunit
        self.rect.move_ip(addx, addy)

        # move rejection for foreground
        while pg.sprite.spritecollide(
            # collide between character and foreground
            self, self.game.layers['foreground'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        ):
            self.rect.move_ip(-xunit, -yunit) # move back 1
    


SPRITE_MAP = DictObj(**{
    "Decal"      : Decal,
    "Block"      : Block,
    "Character"  : Character
})
