import pygame as pg
import yaml

from .sprite import SPRITE_MAP
from .camera import Camera
from .player import Player
from .ossifrage import Ossifrage
from .trigger import Trigger

CLASS_MAP = SPRITE_MAP.copy()
CLASS_MAP['Player'] = Player
CLASS_MAP['Ossifrage'] = Ossifrage
CLASS_MAP['Trigger'] = Trigger


class Scene():
    
    def __init__(self, game, yaml_path):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.data = self.game.load_yaml(yaml_path)
        self.camera = None
        self.player = None
        # TODO add a group single for background sprites
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.SPRITE_GROUPS
        }
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.DRAW_LAYERS
        }
        

        for name in self.data.SPRITE_GROUPS:
            self.groups[name].empty()

        for name in self.data.DRAW_LAYERS:
            layer = self.layers[name]
            layer.empty() # clear out all layers
            if name not in self.data.keys():
                continue
            for sprite_dict in self.data[name]:
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
        self.camera.zoom(self.data.INIT_ZOOM)


    def logic(self, game_input):
        # run all game logic here
        # quit overrides everything else
        if "QUIT" in game_input:
            print("Safely ending game...")
            self.running = False
            return

        if not self.scene: return

        # apply all the input
        for action in game_input:
            self.process_inputs(action)
        
        # update all sprites
        for group_name in self.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()

