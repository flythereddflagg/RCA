import pygame as pg
from .sprite import Character

UP, RIGHT, DOWN, LEFT = (i for i in range(4))

ANIMATIONS = 'animations'
ASSET_PATH = 'asset_path'
KEY_FRAME_SIZE = 'key_frame_size'
KEY_FRAME_TIMES = "key_frame_times"

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        self.todo_list = []
        self.direction = (0, 0)
        if ANIMATIONS in self.options.keys():
            self.init_animation()

    def init_animation(self):
        animation_data = self.options[ANIMATIONS][0]
        # set up animation data
        self.default_image = self.image
        self.animation_image = pg.image.load(animation_data[ASSET_PATH]).convert_alpha()
        self.key_frame_size = [
            i * self.scale for i in animation_data[KEY_FRAME_SIZE]
        ]
        self.n_keyframes = [
            bg // kf for bg, kf in zip(
                self.animation_image.get_rect().size, self.key_frame_size
            )
        ]
        kf_sizex, kf_sizexy = self.key_frame_size
        n_keyframesx, n_keyframesy = self.n_keyframes
        self.key_frame_groups = [
            [
                self.animation_image.subsurface(
                    [kf_sizex * i, kf_sizexy * j] + \
                    self.key_frame_size
                ) for i in range(n_keyframesx)
            ] for j in range(n_keyframesy)
        ]
        self.key_frames = self.key_frame_groups[RIGHT]
        self.key_frame_times = animation_data[KEY_FRAME_TIMES]
        self.key_frame = self.gen_from_list(self.key_frames)
        self.key_frame_time = self.gen_from_list(self.key_frame_times)
        self.frame_time = next(self.key_frame_time)
        self.image = next(self.key_frame)
        self.last_frame_time = 0
        self.last_direction = None

    def update(self):
        for action in self.todo_list:
            self.apply_action(action)
            
        if not self.todo_list:
            self.image = self.default_image
            self.direction = None
            return
        self.animate()

        # reset the todo_list
        self.todo_list = []


    def add_todo(self, action):
        self.todo_list.append(action)


    def animate(self):
        animation_data = self.options[ANIMATIONS][0]
        if self.direction != self.last_direction:
            self.last_direction = self.direction
            self.key_frames = self.key_frame_groups[self.direction]
            self.key_frame_times = animation_data[KEY_FRAME_TIMES]
            self.key_frame = self.gen_from_list(self.key_frames)
            self.key_frame_time = self.gen_from_list(self.key_frame_times)

        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.image = next(self.key_frame)
            self.frame_time = next(self.key_frame_time)
            self.last_frame_time = cur_time
    
    def apply_action(self, action):
        if action in self.game.UNIT_VECTORS.keys():
            direction_vec = self.game.UNIT_VECTORS[action]
            self.move(direction_vec, self.game.dist_per_frame)
            self.last_direction = self.direction
            self.direction = self.game.IND_UNIT_VECTORS[action]
        else:
            print(action + "! (no response)")
            return
        
        # move rejection for foreground
        foreground = self.game.groups[
            self.game.group_enum['foreground']
        ]

        while pg.sprite.spritecollide(
                self, foreground,
                False,
                pg.sprite.collide_mask
        ):
            self.move(direction_vec, -1)

    def gen_from_list(self, item_list):
        while True:
            for item in item_list:
                yield item


