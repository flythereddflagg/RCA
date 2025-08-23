import pygame as pg

from .animation import Animation
from .decal import Decal

class HitMask(Animation):
    # def __init__(self, parent:".node.Node", animation:dict, path_prefix='./'):
    def setup(self):
        sibling_id = self.init.get("sibling")
        assert sibling_id, f"{self.id}: No sibling passed into HitMask"
        sibling_init = self.parent.child_by_id(sibling_id).init

        mask_animation = sibling_init["animation"].copy()
        for key, entry in mask_animation.items():
            entry['datafile'] = entry["hitmask"] if "hitmask" in entry else entry['datafile']
        self.init["animation"] = mask_animation
        self.init["path_prefix"] = sibling_init["path_prefix"]
        super().setup()
        
        self.sprite = Decal(self.scene)

    def update(self):
        super().update()
        
        foreground = self.parent.scene.groups['foreground']
        if self.sprite not in foreground:
            foreground.add(self.sprite)

        self.sprite.rect.topleft = self.parent.sprite.rect.topleft


    def set_frame(self) -> None: # override parent
        current:Frame = (
            self.animation[self.parent.state].frames[self.frame_index]
        )
        new_mask = pg.mask.from_surface(current.image)
        self.sprite.mask = new_mask.scale(
            pg.math.Vector2(new_mask.get_size())*
            self.parent.scene.game.settings.SCALE
        )
        self.frame_time = current.duration
        self.last_set_frame_time = pg.time.get_ticks()