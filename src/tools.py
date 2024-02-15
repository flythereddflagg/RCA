
import yaml
import pygame as pg

from .dict_obj import DictObj

def load_yaml(yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
        return DictObj(**yaml_data)


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