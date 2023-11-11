import pygame as pg
from .sprite import Character

class Player(Character):
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)

    def update(self):
        pass
    
    def apply_action(self, action):
        print(action)
        match action:
            case "UP":
                self.rect.y -= self.game.dist_per_frame
            case "DOWN":
                self.rect.y += self.game.dist_per_frame
            case "LEFT":
                self.rect.x -= self.game.dist_per_frame
            case "RIGHT":
                self.rect.x += self.game.dist_per_frame
            case _:
                print(action + "! (no response)")
        
        # move rejection TODO this is buggy and slow. Need to optimize.
        for sprite in self.game.groups\
            [self.game.group_enum['foreground']]:
            while pg.sprite.collide_mask(self, sprite) is not None:
                # means it collided
                match action:
                    case "UP":
                        self.rect.y += self.game.INIT_ZOOM
                    case "DOWN":
                        self.rect.y -= self.game.INIT_ZOOM
                    case "LEFT":
                        self.rect.x += self.game.INIT_ZOOM
                    case "RIGHT":
                        self.rect.x -= self.game.INIT_ZOOM
                    case _:
                        break

