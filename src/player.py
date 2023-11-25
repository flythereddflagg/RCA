import pygame as pg
from .sprite import Character

UP, RIGHT, DOWN, LEFT = (i for i in range(4))

ANIMATIONS = 'animations'
ASSET_PATH = 'asset_path'
KEY_FRAME_SIZE = 'key_frame_size'
KEY_FRAME_TIMES = "key_frame_times"
DEFAULT_ANIMATION = "walking"

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        self.todo_list = []
        self.direction = (0, 0)
        self.key_frame_group = None
        self.animate_data = None
        if ANIMATIONS in self.options.keys():
            self.init_animation()

    def init_animation(self):
        self.key_frame_groups = {}
        self.animation = {}
        self.default_image = self.image

        for animation in self.options[ANIMATIONS]:
            # load in each animation for a character 
            # defined in their yaml data
            animation_image = pg.image.load(
                animation[ASSET_PATH]
            ).convert_alpha()
            new_size = [
                dim * self.scale 
                for dim in animation_image.get_rect().size
            ]
            animation_image = pg.transform.scale(animation_image, new_size)
            # get the size of each animation frame
            kf_sizex, kf_sizey = [
                i * self.scale for i in animation[KEY_FRAME_SIZE]
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

            self.animation[animation['id']] = animation
            self.animation[animation['id']]['key_frames'] = key_frame_group
            
        # TODO: make it so the group can change  
        self.animate_data = self.animation[DEFAULT_ANIMATION]
        # init dummy default values.
        self.frame_time = 1
        self.last_frame_time = 0
        self.last_direction = None

    def update(self):
        for action in self.todo_list:
            self.apply_action(action)
            
        # TODO add code to set it to stand in whatever direction
        if not self.todo_list:
            self.image = self.default_image

        # reset the todo_list
        self.todo_list = []


    def add_todo(self, action):
        self.todo_list.append(action)


    def animate(self):
        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.image = next(self.key_frame, None)
            self.frame_time = next(self.key_frame_time, None)
            self.last_frame_time = cur_time

        # FIXME: THis breaks the game figure out how to stop this once we run out of frames.
    
    
    
    def apply_action(self, action):
        if action in self.game.UNIT_VECTORS.keys():
            self.animate_data = self.animation['walking']
            direction_vec = self.game.UNIT_VECTORS[action]
            self.move(direction_vec, self.game.dist_per_frame)
            self.last_direction = self.direction
            self.direction = self.game.IND_UNIT_VECTORS[action]
            if self.direction != self.last_direction:
                self.animate_data = self.animation['sword swing']
                self.last_direction = self.direction
                self.key_frames = self.animate_data["key_frames"]
                self.key_frame_times = self.animate_data[KEY_FRAME_TIMES]
                self.key_frame = self.gen_from_list(self.key_frames)
                self.key_frame_time = self.gen_from_list(self.key_frame_times)
            
        elif action == "BUTTON_1":
            print("bUTTON 1")
            self.animate_data = self.animation['sword swing']
            self.last_direction = self.direction
            self.key_frames = self.animate_data["key_frames"]
            self.key_frame_times = self.animate_data[KEY_FRAME_TIMES]
            self.key_frame = self.gen_from_list(self.key_frames, repeat=False)
            self.key_frame_time = self.gen_from_list(self.key_frame_times)

        else:
            print(action + "! (no response)")
            return
        
        # animate if applicable
        if self.key_frame:
            self.animate()

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

    def gen_from_list(self, item_list, repeat=True):
        while True:
            for item in item_list:
                yield item
            if not repeat: break


