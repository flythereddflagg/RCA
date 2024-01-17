class Animation():
    required_animation_keys = [
        'asset_path', 'key_frame_size'
    ]
    def __init__(self, sprite):
        
        self.sprite = sprite
        self.last_animate = None
        self.key_frame_group = None
        self.animate_data = None
        self.key_frame = None
        self.animation_active = False
        self.frame_time = 1
        self.last_frame_time = 0
        self.last_direction = self.direction
        # init animations
        self.key_frame_groups = {}
        self.animation = {}
        self.default_image = self.image
        self.alt_image = Decal(**{
            "id": self.id + "_alt",
            "game": self.scene,
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
                list(map(
                    lambda frame: pg.mask.from_surface(frame),
                    group
                ))
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
            if 'mask' in self.animate_data.keys():
                self.alt_image.mask = next(self.alt_image.mask_set)
        
        if self.image is None: # animation is done
            self.animation_active = False
            last_animate = self.last_animate
            self.last_animate = self.animate_data['id']
            self.animate_data = self.animation[last_animate]
            self.set_key_frame()
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
        


    def set_key_frame(self):
        self.key_frame = self.gen_from_list(
            self.key_frames, repeat=self.animate_data['repeat']
        )
        self.key_frame_time = self.gen_from_list(self.key_frame_times)
        self.set_image(next(self.key_frame, None))
        self.frame_time = next(self.key_frame_time)
        
        if 'mask' in self.animate_data.keys():
            self.alt_image.mask_set = self.gen_from_list(
                self.animate_data['mask'][self.direction]
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