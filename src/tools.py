import importlib
import json

import yaml
import pygame as pg

from .dict_obj import DictObj


def load_yaml(yaml_path) -> DictObj:
    with open(yaml_path) as f:
        yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
    return DictObj(**yaml_data)


def save_yaml(data:dict|list, yaml_path:str):
    yaml_str = yaml.dump(
        data, 
        Dumper=yaml.Dumper, 
        default_flow_style=False, 
        sort_keys=False
    )
    with open(yaml_path, 'w') as f:
        f.write(yaml_str)


def load_json(json_path):
    with open(json_path) as f:
        json_data = json.load(f)
    return DictObj(**json_data)


def mask_collision(self:".decal.Decal", other:".decal.Decal"):
    """
    Tests that both have a valid mask before .
    """
    assert isinstance(self.mask, pg.mask.Mask), \
        f"{self.id} has invlaid mask: {self.mask}"
    assert isinstance(other.mask, pg.mask.Mask), \
        f"{other.id} has invalid mask: {other.mask}"
    
    return pg.sprite.collide_mask(self, other)


def list_collided(
    self:".decal.Decal", other:list[pg.sprite.Sprite]
) -> list[pg.sprite.Sprite]:
    """
    Tests that everyone has a valid mask before
    using returning the collided others.
    """
    assert isinstance(self.mask, pg.mask.Mask), \
        f"{self.id} has invlaid mask: {self.mask}"
    
    for sprite in other:
        assert isinstance(sprite.mask, pg.mask.Mask), \
            f"{sprite.id} has invalid mask: {sprite.mask}"
    return [
        sprite 
        for sprite in other
        if pg.sprite.collide_mask(self, sprite)
    ]


def get_center_screen():
        screen_w, screen_h = pg.display.get_surface().get_size()
        centerx = screen_w // 2
        centery = screen_h // 2
        return (centerx, centery)

def delta_vec(v_from, v_to) -> pg.math.Vector2:
    """
    returns the 2d vector between any two points
    """
    x, y = v_from[0], v_from[1]
    a, b = v_to[0], v_to[1]
    return pg.math.Vector2((a, b)) - pg.math.Vector2((x, y))

def vec(v_input:list|tuple|pg.math.Vector2):
    """convenience function to convert to vector for vector math"""
    return pg.math.Vector2((v_input[0], v_input[1]))


def class_from_str(class_name):
    module_name = "." + class_name.lower()
    module = importlib.import_module(module_name, package='src')
    # get the class, will raise AttributeError if class cannot be found
    class_ref = getattr(module, class_name)
    return class_ref

