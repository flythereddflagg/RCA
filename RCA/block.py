from constants import *
from rca_sprite import SpriteRCA

# see pygame.transform.rotozoom() ?

class Block(SpriteRCA):
    def __init__(self, 
                image_path,
                xposition, 
                yposition,
                scale = 1,
                rotate = 0):
        
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
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
        self.rect.x = xposition
        self.rect.y = yposition
        self.mask = pg.mask.from_surface(self.image)

        
