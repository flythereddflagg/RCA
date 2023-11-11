import pygame as pg


class Camera:
    def __init__(self, game):
        self.game = game
        self.player = self.game.groups\
            [self.game.group_enum['player']].sprites()[0]
        self.mobile_groups = self.game.group_enum.copy()
        del self.mobile_groups['hud']
        del self.mobile_groups['misc']

    def update(self):
        curx, cury = self.player.rect.x, self.player.rect.y
        # if player is inside the cameraslack box, no need to update.
        movex, movey= 0, 0
        if abs(curx - self.game.CENTERX) > self.game.CAMERASLACK:
            e_w = 1 if self.game.CENTERX - curx < 0 else -1
            movex = self.game.CENTERX - curx + e_w * self.game.CAMERASLACK
        if abs(cury - self.game.CENTERY) > self.game.CAMERASLACK:
            n_s = 1 if self.game.CENTERY - cury < 0 else -1
            movey = self.game.CENTERY - cury + n_s * self.game.CAMERASLACK

        if not movex and not movey: return

        # move everything that is moblie to the correct position
        # this simulates moving the camera
        for group, i in self.mobile_groups.items():
            for sprite in self.game.groups[i]:
                sprite.rect.x += movex
                sprite.rect.y += movey

        # TODO add stopping at world border


    def zoom(self, scale):
        for group, i in self.mobile_groups.items():
            for sprite in self.game.groups[i]:
                cur_size = sprite.image.get_rect().size
                new_size = [dim * scale for dim in cur_size]
                sprite.image = pg.transform.scale(sprite.image, new_size)
        
            
