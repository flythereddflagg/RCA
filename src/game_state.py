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
        self.paused = False
        self.current_scene = None
        self.camera = None
        self.INV_KEY_BIND = {v: k for k, v in self.KEY_BIND.items()}
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.SPRITE_GROUPS
        }

    
    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
            print("Safely ending game...")
            self.running = False
            return

        if not self.current_scene: return

        # apply all the input
        for action in game_input:
            self.process_inputs(action)
        
        # update all sprites
        for group_name in self.SPRITE_GROUPS:
            self.groups[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()

    
    def process_inputs(self, action):
        # TODO add more to this so that other characters move and act
        if not self.paused:
            player = self.groups['player'].sprites()[-1]
            player.add_todo(action)


    def load_scene(self, yaml_path):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.current_scene = self.load_yaml(yaml_path)

        for name in self.SPRITE_GROUPS:
            group = self.groups[name]
            group.empty() # clear out all groups
            if name not in self.current_scene.keys():
                continue
            for sprite_dict in self.current_scene[name]:
                sprite_dict['game'] = self
                sprite_instance = CLASS_MAP[sprite_dict['type']](**sprite_dict)
                group.add(sprite_instance)

        self.camera = Camera(self)
        self.camera.zoom(self.INIT_ZOOM)


    @staticmethod    
    def load_yaml(yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
        return DictObj(**yaml_data)
        

