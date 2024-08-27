import pygame as pg

from .tools import get_center_screen
from .node import Node


class Camera(Node):
    def __init__(self, scene):
        super().__init__(scene)
        self.mobile_groups = list(self.scene.layers.keys())
        self.mobile_groups.remove('hud')
        self.cur_zoom = 1

    
    def update(self):
        for sprite in self.scene.all_sprites.sprites():
            if sprite.scale != self.cur_zoom * sprite.init_scale:
                sprite.scale_abs(self.cur_zoom * sprite.init_scale)
        if not self.scene.game.player: return
        self.follow_player()
        if not self.scene.game.DEBUG: self.stop_at_border()


    def pan(self, movex, movey):
        """
        Moves everything mobile to the correct position
        This simulates moving the camera
        """
        if not movex and not movey: return
        for group in self.mobile_groups:
            for sprite in self.scene.layers[group]:
                sprite.rect.move_ip(-movex, -movey)


    def follow_player(self):
        player = self.scene.game.player.sprite
        center = pg.math.Vector2(*get_center_screen())
        player_pos = pg.math.Vector2(player.rect.center)
        movex, movey = player_pos - center
        
        movex, movey = self.add_camera_slack(
            movex, movey, self.scene.data.CAMERASLACK
        )
        self.pan(movex, movey)

    
    def add_camera_slack(self, movex, movey, camera_slack):
        """
        Takes the vector given by (movex, movey) and reduces it by 
        camera slack if either component is greater than camera_slack
        """
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


    def zoom_by(self, factor):
        if factor is None: return
        self.cur_zoom *= factor
        if self.cur_zoom == 0: self.cur_zoom = 1 # 0 resets scale
        background = self.scene.layers['background'].sprites()[0]
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        bg_w, bg_h = background.rect.size
        bg_x, bg_y = background.rect.topleft
        background.scale_by(factor)
        bg_w_new, bg_h_new = background.rect.size
        bg_x_new = centerx - bg_w_new * (centerx - bg_x) / bg_w
        bg_y_new = centery - bg_h_new * (centery - bg_y) / bg_h
        background.rect.topleft = (bg_x_new, bg_y_new)

        for group in self.mobile_groups:
            if group == 'background': continue
            for sprite in self.scene.layers[group]:
                x, y = sprite.rect.center
                sprite.scale_by(factor)
                sprite.rect.center = (
                    bg_x_new + bg_w_new * (x - bg_x) / bg_w, 
                    bg_y_new + bg_h_new * (y - bg_y) / bg_h
                )   

    def zoom_abs(self, scale):
        self.zoom_by(0)
        self.zoom_by(scale)
