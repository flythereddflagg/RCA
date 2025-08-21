import pygame as pg

from .animation import Animation
from .decal import Decal

class HitMask(Animation):
    def __init__(self, parent:".node.Node", animation:dict, path_prefix='./'):
        mask_animation = animation.copy()
        for key, entry in mask_animation.items():
            entry['datafile'] = entry["hitmask"] if "hitmask" in entry else entry['datafile']
        super().__init__(parent, mask_animation, path_prefix)
        
        self.sprite = Decal(self.parent.scene)

    def update(self):
        super().update()
        
        foreground = self.parent.scene.game.scene.groups['foreground']
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