import importlib
import json

import yaml
import pygame as pg

from .dict_obj import DictObj

def filter_serializable(structure:dict|list):
    
    if isinstance(structure, dict):
        generator = structure.items()
        is_dict = True
        output = {}
    elif isinstance(structure, list):
        generator = enumerate(structure)
        is_dict = False
        output = []
    else:
        return None
    
    for key, item in generator:
        if isinstance(item, (str, int, float, bool)) or item is None:
            pass
        elif isinstance(item, (dict, list)):
            # recurse
            item = filter_serializable(item)
        else:
            item = None

        if is_dict:
            output[key] = item
        else:
            output.append(item)
        
    return output



def load_yaml(yaml_path):
    with open(yaml_path) as f:
        yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
    return DictObj(**yaml_data)


def load_json(json_path):
    with open(json_path) as f:
        json_data = json.load(f)
    return DictObj(**json_data)


def mask_collision(self, other):
    """
    Tests that everyone has a valid mask before
    using spritecollideany.
    """
    assert isinstance(self.mask, pg.mask.Mask), \
        f"{self.id} has invlaid mask: {self.mask}"
    for sprite in other.sprites():
        assert isinstance(sprite.mask, pg.mask.Mask), \
            f"{sprite.id} has invalid mask: {sprite.mask}"
    
    if pg.sprite.spritecollideany(self, other, pg.sprite.collide_mask):
        return True
    return False


def list_collided(self, other) -> list:
    """
    Tests that everyone has a valid mask before
    using returning the collided others.
    """
    assert isinstance(self.mask, pg.mask.Mask), \
        f"{self.id} has invlaid mask: {self.mask}"
    for sprite in other.sprites():
        assert isinstance(sprite.mask, pg.mask.Mask), \
            f"{sprite.id} has invalid mask: {sprite.mask}"

    collided_others = pg.sprite.spritecollide(
        self, other, False, pg.sprite.collide_mask
    )
    if collided_others is None: return []
    
    return collided_others


def get_center_screen():
        screen_w, screen_h = pg.display.get_surface().get_size()
        centerx = screen_w // 2
        centery = screen_h // 2
        return (centerx, centery)


def class_from_str(class_name):
    module_name = "." + class_name.lower()
    module = importlib.import_module(module_name, package='src')
    # get the class, will raise AttributeError if class cannot be found
    class_ref = getattr(module, class_name)
    return class_ref

