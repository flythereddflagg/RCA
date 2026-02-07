import copy
import pygame as pg

from .animation import Animation
from .decal import Decal

class HitMask(Animation):
    def setup(self):
        self.require_attr("sibling", "kind")
        sibling_id = self.init["sibling"]
        kind = self.init["kind"]
        sibling_init = self.parent.child_by_id(sibling_id).init

        # deep copy is necessary to avoid overwriting the animation
        mask_animation = copy.deepcopy(sibling_init["animation"])
        for key, entry in mask_animation.items():
            entry["datafile"] = (
                entry[kind] 
                if kind in entry else 
                ""
            )

        self.init["animation"] = mask_animation
        self.init["path_prefix"] = sibling_init["path_prefix"]
        self.init["default_state"] = sibling_init["default_state"]
        super().setup()
        
        self.add_child(Decal(id="sprite"))

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
        self.sprite.set_image(mask=new_mask)
        self.frame_time = current.duration
        self.last_set_frame_time = pg.time.get_ticks()
    
