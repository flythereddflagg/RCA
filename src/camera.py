import pygame as pg


class Camera:
    def __init__(self, game):
        self.scene = game
        self.player = None
        self.mobile_groups = list(self.scene.layers.keys())
        self.mobile_groups.remove('hud')
        self.cur_zoom = 1
        # TODO extract mobile groups to data files so it can be set there
        # TODO LOW set in game zoom
        


    def update(self):
        self.follow_player()
        self.stop_at_border()


    def pan(self, movex, movey):
        if not movex and not movey: return
        # move everything that is mobile to the correct position
        # this simulates moving the camera
        for group in self.mobile_groups:
            for sprite in self.scene.layers[group]:
                sprite.rect.move_ip(-movex, -movey)


    def follow_player(self):
        if not self.player: return
        # get the current center of the screen
        screen_w, screen_h = pg.display.get_surface().get_size()
        centerx = screen_w // 2
        centery = screen_h // 2
        center = pg.math.Vector2(centerx, centery)
        player_pos = pg.math.Vector2(self.player.rect.center)
        movex, movey = player_pos - center
        
        movex, movey = self.add_camera_slack(
            movex, movey, self.scene.data.CAMERASLACK
        )
        self.pan(movex, movey)

    
    def add_camera_slack(self, movex, movey, camera_slack):
        """takes the vector given by (movex, movey) and reduces it by 
        camera slack if either component is greater than camera_slack"""
        if abs(movex) > camera_slack:
            pos_neg = 1 if movex > 0 else -1
            movex = pos_neg * (abs(movex) - camera_slack)
        else: movex = 0
        if abs(movey) > camera_slack:
            pos_neg = 1 if movey > 0 else -1
            movey = pos_neg * (abs(movey) - camera_slack)
        else: movey = 0
        
        return movex, movey


    def stop_at_border(self):
        screen_w, screen_h = pg.display.get_surface().get_size()
        background = self.scene.layers['background'].sprites()[0]

        # if background is too small then just return without modifying
        background_w, background_h = background.rect.size
        if background_w < screen_w or background_h < screen_h: return

        backx, backy = 0, 0
        if background.rect.left > 0:
            backx = background.rect.left
        elif background.rect.right < screen_w:
            backx = background.rect.right - screen_w

        if background.rect.top > 0:
            backy = background.rect.top
        elif background.rect.bottom< screen_h:
            backy = background.rect.bottom - screen_h

        self.pan(backx, backy)


    def center_player(self):
        tmp_storage = self.scene.data.CAMERASLACK
        self.scene.data.CAMERASLACK = 0
        self.follow_player()
        self.scene.data.CAMERASLACK = tmp_storage


    def zoom(self, factor):
        self.cur_zoom *= factor
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
        
            
