import pygame as pg
import yaml

from .dict_obj import DictObj
from .sprite import SPRITE_MAP
from .camera import Camera
from .player import Player

CLASS_MAP = SPRITE_MAP.copy()
CLASS_MAP['Player'] = Player


class GameState(DictObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False
        self.SCREENSIZE = (self.SCREENWIDTH, self.SCREENHEIGHT)
        # x and y coordinates for the center of the screen
        self.CENTERX = self.SCREENWIDTH  // 2 
        self.CENTERY = self.SCREENHEIGHT // 2
        self.INV_KEY_BINDINGS = {
           item:key for key, item in self.KEY_BINDINGS.items()
        }

        self.dist_per_frame = self.PLAYERPEED / self.FPS
        self.groups = [
            pg.sprite.Group() 
            for i in self.SPRITE_GROUPS
        ]
        self.group_enum = {
            group:i for i, group in enumerate(self.SPRITE_GROUPS)
        }
        self.current_scene = None
        self.paused = False

    
    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
            print("Safely ending game...")
            self.running = False
            return

        # apply all the input
        for action in game_input:
            self.process_inputs(action)
        
        # update all sprites
        for group in self.groups:
            group.update()
        
        # finally, update the camera
        self.camera.update()

    
    def process_inputs(self, action):
        # TODO add more to this so that other characters move and act
        if not self.paused:
            player = self.groups[self.group_enum['player']].sprites()[0]
            player.add_todo(action)


    def load_scene(self, yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)

        self.current_scene = DictObj(**yaml_data)

        for name, group in zip(self.SPRITE_GROUPS, self.groups):
            group.empty() # clear out all groups
            if name not in self.current_scene.keys():
                continue
            for sprite_dict in self.current_scene[name]:
                sprite_dict['game'] = self
                sprite_type = sprite_dict["type"]
                sprite_instance = CLASS_MAP[sprite_type](**sprite_dict)
                group.add(sprite_instance)

        self.camera = Camera(self)
        self.camera.zoom(self.INIT_ZOOM)
        

