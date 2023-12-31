import pygame as pg
import yaml

from .dict_obj import DictObj
from .scene import Scene


class GameState(DictObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dt = 1
        self.running = False
        self.paused = False
        self.scene = None
        self.INV_KEY_BIND = {v: k for k, v in self.KEY_BIND.items()}

    
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
        for group_name in self.scene.data.DRAW_LAYERS:
            self.scene.layers[group_name].update()
        
        # finally, update the camera
        if self.scene.camera: self.scene.camera.update()

    
    def process_inputs(self, action):
        if not self.paused and self.scene.player:
            self.scene.player.add_todo(action)


    def load_scene(self, yaml_path):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.scene = Scene(self, yaml_path)


    @staticmethod
    def load_yaml(yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
        return DictObj(**yaml_data)
