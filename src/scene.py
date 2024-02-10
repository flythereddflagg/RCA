import pygame as pg

from .tools import load_yaml

from .dict_obj import DictObj
from .camera import Camera
from .decal import Decal
from .player import Player
from .ossifrage import Ossifrage
from .edge import Edge

SPRITE_MAP = DictObj(**{
    "Decal"      : Decal,
    'Player': Player,
    'Ossifrage': Ossifrage,
    'Edge': Edge,
})



class Scene():
    
    def __init__(self, game, yaml_path, player_path=None):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.data = load_yaml(yaml_path)

        
        # TODO add a group single for background sprites
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.SPRITE_GROUPS
        }
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.DRAW_LAYERS
        }
        

        for name in self.data.DRAW_LAYERS:
            layer = self.layers[name]
            layer.empty() # clear out all layers
            if name not in self.data.keys():
                continue
            for sprite_dict in self.data[name]:
                sprite_dict['scene'] = self
                sprite_instance = SPRITE_MAP[sprite_dict['type']](**sprite_dict)
                layer.add(sprite_instance)
                if "groups" in sprite_instance.options.keys():
                    for group in sprite_instance.options['groups']:
                        self.groups[group].add(sprite_instance)
        
        self.camera = Camera(self)
        # self.camera.zoom(self.data.INIT_ZOOM)
        # FIXME zoom is broken
        
        if player_path:
            player_data = load_yaml(player_path)
            player_data['scene'] = self
            self.player = SPRITE_MAP[player_data['type']](**player_data)
            if "groups" in self.player.options.keys():
                    for group in self.player.options['groups']:
                        self.groups[group].add(self.player)
            self.layers['foreground'].add(self.player)
            self.camera.player = self.player
        else:
            self.player = None

        
    def update(self):
        
        # update all sprites
        for group_name in self.data.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()


