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
        self.key_frame_groups = {}
        if ANIMATIONS in self.options.keys():
            self.init_animation()

    def init_animation(self):
        self.default_image = self.image

        for animation_data in self.options[ANIMATIONS]:
            # load in each animation for a character 
            # defined in their yaml data
            animation_image = pg.image.load(
                animation_data[ASSET_PATH]
            ).convert_alpha()
            new_size = [
                dim * self.scale 
                for dim in animation_image.get_rect().size
            ]
            animation_image = pg.transform.scale(animation_image, new_size)
            # get the size of each animation frame
            kf_sizex, kf_sizey = [
                i * self.scale for i in animation_data[KEY_FRAME_SIZE]
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

            self.key_frame_groups[animation_data['id']] = key_frame_group

        # select the first group TODO make it so this can change
        self.key_frame_group = self.key_frame_groups["walking"] 
        # init dummy default values.
        self.frame_time = 1
        self.last_frame_time = 0
        self.last_direction = None

    def update(self):
        for action in self.todo_list:
            self.apply_action(action)
            
        if not self.todo_list:
            self.image = self.default_image
            return
        if self.key_frame_groups:
            self.animate()

        # reset the todo_list
        self.todo_list = []


    def add_todo(self, action):
        self.todo_list.append(action)


    def animate(self):
        animation_data = self.options[ANIMATIONS][0]
        if self.direction != self.last_direction:
            self.last_direction = self.direction
            self.key_frames = self.key_frame_group[self.direction]
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


