from constants import *
from rca_sprite import SpriteRCA


class Block(SpriteRCA):
    def __init__(self, 
            img_path, # ="./sprites/blocks/rock.png"
            xpos, 
            ypos,
            scale = 1,
            rotate = 0):
        
        super().__init__()
        self.image = pg.image.load(img_path).convert_alpha()
        # see pygame.transform.rotozoom() ?
        if scale != 1:
            width, height = self.image.get_size()
            width *= scale
            height *= scale
            self.image = pg.transform.scale(
                self.image, 
                (int(width), int(height)))
        if rotate != 0:
            self.image = pg.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
