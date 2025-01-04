import pygame as pg

from .animation import Animation

class HitMask(Animation):
    def __init__(self, parent, animations:dict, path_prefix='./'):
        mask_animations = animations.copy()
        for key, entry in mask_animations.items():
            entry['datafile'] = entry["hitmask"] if "hitmask" in entry else entry['datafile']
        super().__init__(parent, mask_animations, path_prefix)
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.surface.Surface((32, 32), flags=pg.SRCALPHA)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.mask = None

    def update(self):
        super().update()
        
        foreground = self.parent.game.scene.layers['foreground']
        if self.sprite not in foreground:
            foreground.add(self.sprite)

        self.sprite.rect.topleft = self.parent.sprite.rect.topleft


    def set_frame(self) -> None: # override parent
        current:Frame = (
            self.animations[self.parent.state].frames[self.frame_index]
        )
        new_mask = pg.mask.from_surface(current.image)
        self.sprite.mask = new_mask.scale(
            pg.math.Vector2(new_mask.get_size())*self.parent.game.SCALE
        )
        self.frame_time = current.duration
        self.last_set_frame_time = pg.time.get_ticks()