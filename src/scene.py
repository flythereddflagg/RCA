import pygame as pg

from .tools import load_yaml, class_from_str
from .camera import Camera


class Scene():  
    def __init__(self, game, yaml_path, player=None):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.data = load_yaml(yaml_path)
        self.all_sprites = pg.sprite.Group()
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.SPRITE_GROUPS
        }
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.DRAW_LAYERS
        }
        self.layers['hud'] = pg.sprite.Group() # hud is a given
        
        for name, layer in self.layers.items():
            layer_data = self.data.get(name)
            if not layer_data: continue

            for node_init in layer_data:
                node_init['scene'] = self
                yaml = node_init.get("yaml")
                if yaml: node_init = {**node_init, **load_yaml(yaml)}
                class_str = node_init['type']
                node = class_from_str(class_str)(**node_init)
                sprite_instance = (
                    node 
                    if isinstance(node, pg.sprite.Sprite) else 
                    node.sprite
                )
                self.all_sprites.add(sprite_instance)
                layer.add(sprite_instance)
                groups = node_init.get('groups')
                if groups:
                    for group in groups:
                        self.groups[group].add(sprite_instance)
                
                start = node_init.get('start')
                if start:
                    sprite_instance.rect.center = start
                
                # TODO add yaml loading for more complex stuff!

        
        self.camera = Camera(self)

        self.game.player = self.load_player(player)


    def update(self):        
        # update all sprites
        for group_name in self.data.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()


    def load_player(self, player_init) -> object:
        if not player_init: return None

        if isinstance(player_init, str) and player_init.endswith(".yaml"):
            player_data = load_yaml(player_init)
            player_data['scene'] = self
            player = (
                class_from_str(player_data['type'])(**player_data)
            )
            sprite_instance = (
                player 
                if isinstance(player, pg.sprite.Sprite) else 
                player.sprite
            )
            groups = player_data.get('groups')
            if groups:
                for group in groups:
                    self.groups[group].add(sprite_instance)
            
            start = player_data.get('start')
            if start:
                sprite_instance.rect.center = start
            self.layers['foreground'].add(player.sprite)
            self.camera.player = player
        elif isinstance(player_init, object):
            player = player_init
            player.set_scale(0) # reset player scale
            player.set_scale(self.game.SCALE)
            player.scene = self
            self.layers['foreground'].add(player)
            self.groups['player'].add(player)
            player.animation.previous = ''
            self.camera.player = player
        else:
            raise TypeError(
                f"Player {player_init} is of Type {type(player)}! Should be str or object"
            )
        return player
