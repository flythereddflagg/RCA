import pygame as pg



class Camera:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.mobile_groups = list(self.game.layers.keys())
        self.mobile_groups.remove('hud')

    def update(self):
        # get the current center of the screen
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        # get current player position
        curx, cury = self.player.rect.x, self.player.rect.y

        # if player is inside the cameraslack box, no need to update.
        movex, movey= 0, 0
        if abs(curx - centerx) > self.game.CAMERASLACK:
            e_w = 1 if centerx - curx < 0 else -1
            movex = centerx - curx + e_w * self.game.CAMERASLACK
        if abs(cury - centery) > self.game.CAMERASLACK:
            n_s = 1 if centery - cury < 0 else -1
            movey = centery - cury + n_s * self.game.CAMERASLACK
        
        movex, movey = self.stop_at_border(movex, movey)

        if not movex and not movey: return

        # move everything that is moblie to the correct position
        # this simulates moving the camera
        for group in self.mobile_groups:
            for sprite in self.game.layers[group]:
                sprite.rect.x += movex
                sprite.rect.y += movey
        
        
    def stop_at_border(self, movex, movey):
        """
        Stop at world border. Adjust movex and movey
        to avoid seeing the void at the world border.
        """
        # check if world border is visible then set to screen border
        old_movex, old_movey =  movex, movey
        screen_w, screen_h = pg.display.get_surface().get_size()
        background = self.game.layers['background'].sprites()[0]

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
        
        # if the background is too small for the screen, 
        # turn off stopping at border
        if background.rect.size[0] < screen_w: movex = old_movex
        if background.rect.size[1] < screen_h: movey = old_movey

        return movex, movey


    def zoom(self, scale):
        # FIXME: if used continuously, this will break sprites. 
        
        for group in self.mobile_groups:
            for sprite in self.game.layers[group]:
                cur_size = sprite.image.get_rect().size
                new_size = [dim * scale for dim in cur_size]
                sprite.image = pg.transform.scale(sprite.image, new_size)
                sprite.mask = pg.mask.from_surface(sprite.image)
        
            
