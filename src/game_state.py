import pygame as pg
import yaml

from .dict_obj import DictObj
from .sprite import SPRITE_MAP
from .camera import Camera
from .player import Player
from .ossifrage import Ossifrage
from .trigger import Trigger

CLASS_MAP = SPRITE_MAP.copy()
CLASS_MAP['Player'] = Player
CLASS_MAP['Ossifrage'] = Ossifrage
CLASS_MAP['Trigger'] = Trigger



class GameState(DictObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dt = 1
        self.running = False
        self.paused = False
        self.current_scene = None
        self.camera = None
        self.player = None
        self.INV_KEY_BIND = {v: k for k, v in self.KEY_BIND.items()}
        # TODO add a group single for background sprites
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.SPRITE_GROUPS
        }
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.DRAW_LAYERS
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
        for group_name in self.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()

    
    def process_inputs(self, action):
        # TODO add more to this so that other characters move and act
        if not self.paused and self.player:
            self.player.add_todo(action)


    def load_scene(self, yaml_path):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.current_scene = self.load_yaml(yaml_path)

        for name in self.SPRITE_GROUPS:
            self.groups[name].empty()

        for name in self.DRAW_LAYERS:
            layer = self.layers[name]
            layer.empty() # clear out all layers
            if name not in self.current_scene.keys():
                continue
            for sprite_dict in self.current_scene[name]:
                sprite_dict['game'] = self
                sprite_instance = CLASS_MAP[sprite_dict['type']](**sprite_dict)
                if sprite_instance.id == "PLAYER":
                    self.player = sprite_instance
                layer.add(sprite_instance)
                if "group_add" in sprite_instance.options.keys():
                    for group in sprite_instance.options['group_add']:
                        self.groups[group].add(sprite_instance)
                if isinstance(sprite_instance, CLASS_MAP['Character']):
                    for group in sprite_instance.groups():
                        layer.add(sprite_instance.alt_image)

        self.camera = Camera(self)
        self.camera.zoom(self.INIT_ZOOM)



    @staticmethod    
    def load_yaml(yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
        return DictObj(**yaml_data)
        

