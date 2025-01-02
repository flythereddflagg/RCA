import pygame as pg

from .node import Node

class HitMask(Node):
    def __init__(self, parent, **options):
        super().__init__(options)
        self.parent = parent
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.surface.Surface((32, 32), flags=pg.SRCALPHA)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.mask = None
        self.mask = pg.mask.from_surface(pg.image.load("./assets/actor/larry/frame_mask.png").convert_alpha())
        self.mask = self.mask.scale(
            pg.math.Vector2(self.mask.get_size())*self.parent.game.SCALE
        )

    def update(self):
        if self.parent.state == 'sword':
            self.sprite.mask = self.mask
        else:
            self.sprite.mask = None
        
        # TODO improve upon this temporary solution to the hit mask problem
        foreground = self.parent.game.scene.layers['foreground']
        if self.sprite not in foreground:
            foreground.add(self.sprite)

        self.sprite.rect.topleft = (
            # self.parent.sprite.rect.topleft + pg.math.Vector2(32,32)
            self.parent.sprite.rect.topleft
        )
