import pygame as pg

from .edge import Edge
from .decal import Decal

class EdgeEnd(Edge):
    def exec_trigger(self):
        # super().exec_trigger()
        end_text = pg.font.SysFont("Sans", 22)
        surface = end_text.render(
            "YOU WIN!!! (Press backspace to quit.)", 
            True, (255,255,255)
        )
        sprite = Decal(parent=self)
        sprite.image = surface
        sprite.rect = surface.get_rect()
        sprite.rect.center = self.scene.game.get_center()
        self.scene.hud.add(sprite)
        self.kill()
        self.scene.get_player().kill()
        
