import pygame as pg

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.image = None
        self.rect = None

    def update(self):
        print("WARNING: update_function has not been overriden.")
        if self.image is None or self.rect is None:
            raise NotImplementedError(
                "'image' and 'rect' attributes MUST be defined."
            )


class Player(BaseSprite):
    def __init__(self):
        super().__init__()
        self.asset_path = "./assets/dummy/character.png"
        self.image = pg.image.load(self.asset_path).convert_alpha()
        self.rect = self.image.get_rect()
    
    def update(self):
        pass