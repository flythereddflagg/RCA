import pygame as pg
from .sprite import Character
from .compass import Compass

DEFAULT_ANIMATION = 'stand'

class Player(Character):
    def __init__(self, **options):
        super().__init__(**options)
        self.todo_list = []
        self.last_animate = None
        self.key_frame_group = None
        self.animate_data = None
        self.last_direction = None
        self.key_frame = None
        self.animation_availible = False
        self.animation_active = False
        self.frame_time = 1
        self.last_frame_time = 0
        self.direction = Compass.DOWN
        self.last_direction = self.direction
        # TODO: redo speeds in terms of subpixels so this can scale
        self.PLAYERSPEED = 300 # pixels per second
        self.dist_per_frame = self.PLAYERSPEED // self.game.FPS
        # init animations
        self.animation_availible = True
        self.key_frame_groups = {}
        self.animation = {}
        self.default_image = self.image

        for animation in self.options['animations']:
            # load in each animation for a character 
            # defined in their yaml data
            animation_image = pg.image.load(
                animation['asset_path']
            ).convert_alpha()
            new_size = [
                dim * self.scale 
                for dim in animation_image.get_rect().size
            ]
            animation_image = pg.transform.scale(animation_image, new_size)
            # get the size of each animation frame
            kf_sizex, kf_sizey = [
                i * self.scale for i in animation['key_frame_size']
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
            self.animation[animation['id']] = animation
            self.animation[animation['id']]['key_frames'] = key_frame_group
            
        # TODO: make it so the group can change  
        self.animate_data = self.animation[DEFAULT_ANIMATION]


    def update(self):
        for action in self.todo_list:
            self.apply_action(action)

        if not self.todo_list and not self.animation_active:
            self.animate_data = self.animation['stand']

        # animate if applicable
        if self.animation_availible:
            self.animate()

        # reset the todo_list
        self.todo_list = []


    def add_todo(self, action):
        self.todo_list.append(action)


    def set_key_frame(self):
        self.key_frame = self.gen_from_list(self.key_frames, 
            repeat=self.animate_data['repeat']
        )
        self.key_frame_time = self.gen_from_list(self.key_frame_times)
        self.set_image(next(self.key_frame, None))
        self.frame_time = next(self.key_frame_time)

    def set_image(self, image):
        # TODO this works but you can clip through walls. Try to make it so you don't do that.
        center = self.rect.center 
        self.image = image
        
        if image is None: return
        self.rect = image.get_rect()
        self.rect.center = center


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

        # check if a frame should be updated
        # if self.frame_time == 0:
        #     return
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

    

    def apply_action(self, action):
        if self.animation_active: return

        if action in Compass.strings: 
            # ^ means a direction button is being pressed
            self.move(Compass.vec_map[action], self.dist_per_frame)
            self.direction = Compass.i_map[action]
            self.animate_data = self.animation['walk']
            
            # move rejection for foreground
            while pg.sprite.spritecollide(
                # collide between player and foreground
                self, self.game.groups['foreground'], 
                # do not kill, use the masks for collision
                False, pg.sprite.collide_mask
            ):
                self.move(Compass.vec_map[action], -1) # move back
            
        elif action == "BUTTON_1":
            self.animation_active = True
            self.animate_data = self.animation['sword swing']


        else:
            print(action + "! (no response)")
            return

    def gen_from_list(self, item_list, repeat=True):
        while True:
            for item in item_list:
                yield item
            if not repeat: break
