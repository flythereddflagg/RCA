import pygame as pg

from .edge import Edge
from .tools import get_center_screen

class EdgeEnd(Edge):
    def exec_trigger(self):
        # super().exec_trigger()
        end_text = pg.font.SysFont("Sans", 44)
        surface = end_text.render("YOU WIN!!! (Press backspace to quit.)", True, (255,255,255))
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.mask = pg.mask.Mask(size=(32, 32), fill=False)
        sprite.rect = surface.get_rect()
        sprite.rect.center = get_center_screen()
        self.scene.hud.add(sprite)
        self.kill()
        self.scene..sprites()[0].sprite.kill()
        
