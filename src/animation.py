import operator

class Animation():
    required_animation_keys = [
        'asset_path', 'frame_size'
    ]
    def __init__(self, sprite, **options):
        
        self.sprite = sprite
        self.frames = {} # a dict of 

        self.last_animate = None
        self.frame_group = None
        self.data = None
        self.frame = None
        self.animation_active = False
        self.frame_time = 1
        self.last_frame_time = 0
        self.last_direction = self.sprite.direction
        # init animations
        self.frame_groups = {}
        self.animation = {}
        self.default_image = self.image
        self.active = False


        for animation in self.options['animations']:
            # load in each animation for a character 
            # defined in their yaml data
            animation['frames'] = self.parse_animation(
                animation['asset_path'], animation['key_frame_size']
            )
            # add a special mask if it exists
            if 'mask_path' in animation:
                animation['mask'] = self.parse_animation(
                    animation['mask_path'], animation['key_frame_size'],
                    make_mask=True
                )
            self.animation[animation['id']] =  animation


             
        self.data = self.animation[DEFAULT_ANIMATION]
        self.null_image = self.animation['null']['frames'][0][0]

        
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
        if self.data['id'] != self.last_animate:
            set_frame = True
            self.last_animate = self.data['id']
            self.frames = self.data["frames"][self.direction]
            self.frame_times = self.data['frame_times']

        # update direction if it has changed
        if self.direction != self.last_direction:
            set_frame = True
            self.last_direction = self.direction
            self.frames = self.data["frames"][self.direction]
        
        if set_frame: self.set_frame()

        # if enough time has passed, set the new image
        cur_time = pg.time.get_ticks()
        for _ in range((cur_time -  self.last_frame_time) // self.frame_time):
            self.set_image(next(self.frame, None))
            self.frame_time = next(self.frame_time)
            self.last_frame_time = cur_time
            if 'mask' in self.data.keys():
                self.alt_image.mask = next(self.alt_image.mask_set)
        
        if self.image is None: # animation is done
            self.animation_active = False
            last_animate = self.last_animate
            self.last_animate = self.data['id']
            self.data = self.animation[last_animate]
            self.set_frame()
            self.alt_image.mask = None


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
        


    def set_frame(self):
        self.frame = self.gen_from_list(
            self.frames, repeat=self.data['repeat']
        )
        self.frame_time = self.gen_from_list(self.frame_times)
        self.set_image(next(self.frame, None))
        self.frame_time = next(self.frame_time)
        
        if 'mask' in self.data.keys():
            self.alt_image.mask_set = self.gen_from_list(
                self.data['mask'][self.direction]
            )
            self.alt_image.mask = next(self.alt_image.mask_set)
            


    def gen_from_list(self, item_list, repeat=True):
        """
        generator for images. Repeats forever unless told otherwise.
        """
        while True:
            for item in item_list:
                yield item
            if not repeat: break
