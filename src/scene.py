import pygame as pg
import yaml

from .dict_obj import DictObj
from .camera import Camera
from .decal import Decal
from .character import Character
from .player import Player
from .ossifrage import Ossifrage
from .edge import Edge

SPRITE_MAP = DictObj(**{
    "Decal"      : Decal,
    "Character"  : Character,
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
        self.data = self.game.load_yaml(yaml_path)

        
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
                if "group_add" in sprite_instance.options.keys():
                    for group in sprite_instance.options['group_add']:
                        self.groups[group].add(sprite_instance)
        
        self.camera = Camera(self)
        self.camera.zoom(self.data.INIT_ZOOM)
        
        if player_path:
            player_data = self.game.load_yaml(player_path)
            player_data['scene'] = self
            self.player = SPRITE_MAP[player_data['type']](**player_data)
            if "group_add" in self.player.options.keys():
                    for group in self.player.options['group_add']:
                        self.groups[group].add(self.player)
            self.layers['characters'].add(self.player)
            self.camera.player = self.player
        else:
            self.player = None

        
    def update(self):
        
        # update all sprites
        for group_name in self.data.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()

    @classmethod
    def load_scene(cls, cur_scene, game, yaml_path):
        new_scene = cls(game, yaml_path)
        game.scene = new_scene
        new_scene.camera.player = cur_scene.player
        return new_scene
    # TODO implement and test this method
