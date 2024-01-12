import pygame as pg

### FIXME this is test code
def inf_gen(iter_):
    while True:
        for thing in iter_:
            yield thing
SCALE_RUN = 1.05
FACTOR = inf_gen([SCALE_RUN, 1/SCALE_RUN])
### FIXME this is test code

class Camera:
    def __init__(self, game):
        self.scene = game
        self.player = self.scene.player
        self.mobile_groups = list(self.scene.layers.keys())
        self.mobile_groups.remove('hud')
        self.cur_zoom = 1
        self.last_time = 0 # FIXME this is test code
        self.next_factor = 1 # FIXME this is test code

    def update(self):
        ### FIXME this is test code
        # curtime = pg.time.get_ticks()
        # if curtime - self.last_time > 1000:
        #     self.last_time = curtime
        #     self.next_factor = next(FACTOR)
            
        # self.zoom(self.next_factor)
        # print(self.cur_zoom)
        ### FIXME END this is test code

        self.follow_player()

    def follow_player(self):
        if not self.player: return
        # get the current center of the screen
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        # get current player position
        curx, cury = self.player.rect.center

        # if player is inside the cameraslack box, no need to update.
        movex, movey= 0, 0
        if abs(curx - centerx) > self.scene.data.CAMERASLACK:
            e_w = 1 if centerx - curx < 0 else -1
            movex = centerx - curx + e_w * self.scene.data.CAMERASLACK
        if abs(cury - centery) > self.scene.data.CAMERASLACK:
            n_s = 1 if centery - cury < 0 else -1
            movey = centery - cury + n_s * self.scene.data.CAMERASLACK
        
        movex, movey = self.stop_at_border(movex, movey)

        if not movex and not movey: return

        # move everything that is moblie to the correct position
        # this simulates moving the camera
        for group in self.mobile_groups:
            for sprite in self.scene.layers[group]:
                sprite.rect.x += movex
                sprite.rect.y += movey
        
    def center_player(self):
        tmp_storage = self.scene.data.CAMERASLACK
        self.scene.data.CAMERASLACK = 0
        self.follow_player()
        self.scene.data.CAMERASLACK = tmp_storage


    def stop_at_border(self, movex, movey):
        """
        Stop at world border. Adjust movex and movey
        to avoid seeing the void at the world border.
        """
        # check if world border is visible then set to screen border
        old_movex, old_movey =  movex, movey
        screen_w, screen_h = pg.display.get_surface().get_size()
        background = self.scene.layers['background'].sprites()[0]

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


    def zoom(self, factor):
        self.cur_zoom *= factor
        self.center_player()
        background = self.scene.layers['background'].sprites()[0]
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        bg_w, bg_h = background.rect.size
        bg_x, bg_y = background.rect.topleft
        background.set_scale(factor)
        bg_w_new, bg_h_new = background.rect.size
        bg_x_new = centerx - bg_w_new * (centerx - bg_x) / bg_w
        bg_y_new = centery - bg_h_new * (centery - bg_y) / bg_h
        background.rect.topleft = (bg_x_new, bg_y_new)

        for group in self.mobile_groups:
            if group == 'background': continue
            for sprite in self.scene.layers[group]:
                x, y = sprite.rect.center
                sprite.set_scale(factor)
                sprite.rect.center = (
                    bg_x_new + bg_w_new * (x - bg_x) / bg_w, 
                    bg_y_new + bg_h_new * (y - bg_y) / bg_h
                )
        
            
