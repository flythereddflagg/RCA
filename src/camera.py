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
        
        movex, movey = self.stop_at_border(movex, movey)

        if not movex and not movey: return

        # move everything that is moblie to the correct position
        # this simulates moving the camera
        for group, i in self.mobile_groups.items():
            for sprite in self.game.groups[i]:
                sprite.rect.x += movex
                sprite.rect.y += movey
        
        
    def stop_at_border(self, movex, movey):
        """
        Stop at world border. Adjust movex and movey
        to avoid seeing the void at the world border.
        """
        # check if world border is visible then set to screen border
        screen_w, screen_h = pg.display.get_surface().get_size()
        background = self.game.groups[
            self.game.group_enum['background']
        ].sprites()[0]
        # in the x direction
        if (background.rect.left + movex > 0 or\
            background.rect.right + movex < screen_w
        ):
            movex = -background.rect.left \
                if background.rect.left + movex > 0\
                else screen_w - background.rect.right
        # and in the y direction
        if (background.rect.top + movey > 0 or\
            background.rect.bottom + movey < screen_h
        ):
            movey = -background.rect.top \
                if background.rect.top + movey > 0\
                else screen_h - background.rect.bottom
        
        return movex, movey


    def zoom(self, scale):
        # if used continuously, this will break sprites. TODO fix this?
        
        for group, i in self.mobile_groups.items():
            for sprite in self.game.groups[i]:
                cur_size = sprite.image.get_rect().size
                new_size = [dim * scale for dim in cur_size]
                sprite.image = pg.transform.scale(sprite.image, new_size)
                sprite.mask = pg.mask.from_surface(sprite.image)
        
            
