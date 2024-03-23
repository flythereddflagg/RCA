
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


def list_collided(self, other):
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

