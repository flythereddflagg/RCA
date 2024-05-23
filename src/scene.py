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
        
        for name, layer in self.layers.items():
            layer_data = self.data.get(name)
            if not layer_data: continue

            for entity_init in layer_data:
                entity_init['scene'] = self
                class_str = entity_init['type']
                entity = class_from_str(class_str)(**entity_init)
                sprite_instance = (
                    entity 
                    if isinstance(entity, pg.sprite.Sprite) else 
                    entity.sprite
                )
                layer.add(sprite_instance)
                groups = entity_init.get('groups')
                if groups:
                    for group in groups:
                        self.groups[group].add(sprite_instance)
                
                start = entity_init.get('start')
                if start:
                    sprite_instance.rect.center = start
                
                # TODO add yaml loading for more complex stuff!

        
        self.camera = Camera(self)


    def update(self):
        pass
