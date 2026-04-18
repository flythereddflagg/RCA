import random

import pygame as pg

from .node import Node
from .tools import vec, diff_vec

# TODO -3- make adaptive camera the follows the player and gives them better FOV in the direction they are facing.


class Camera(Node):
    
    def setup(self):
        self.mobile_groups = self.scene.draw_layers.copy()
        self.mobile_groups.remove('hud')
        self.cur_zoom = 1
        self.slack = self.init.get("slack", 0) 
        self.zoom_by(self.init.get("zoom", 1))
        self.shaking = False
        self.path = []
        

    def update(self):
        player = self.scene.get_player()
        if not player:
            # if there is no player, 
            # move the camera to put the background topleft at 0,0
            movex, movey = self.scene.bg_ref.sprite.rect.topleft
            self.pan(movex, movey)
            return
        self.follow_player()
        if self.shaking:
            cur_move = next(self.path, None)
            if cur_move is None:
                self.shaking = False
                self.path = iter([])
            else:
                self.pan(*cur_move)
            
        if not self.scene.game.settings.DEBUG: 
            self.stop_at_border()


    def pan(self, movex, movey):
        """
        Moves everything mobile in the negative x and y directions
        by movex and movey pixels respectively.
        This simulates moving the camera
        """
        if not movex and not movey: return
        for group in self.mobile_groups:
            for sprite in self.scene.groups[group]:
                sprite.rect.move_ip(-movex, -movey)


    def screenshake(self, length=1, scale=20):
        """@length is in seconds"""
        self.shaking = True
        self.path = iter([
            [random.random()*scale-scale/2 for _ in range(2)] 
            for _ in range(int(length * self.scene.game.clock.get_fps()))
        ])


    def follow_player(self):
        player = self.scene.get_player().sprite
        movex, movey = diff_vec(
            player.rect.center, 
            # player.rect.topleft, 
            self.scene.game.get_center()
        )
        
        movex, movey = self.add_slack(
            movex, movey, self.slack
        )
        self.pan(movex, movey)

    
    def add_slack(self, movex, movey, slack):
        """
        Takes the vector given by (movex, movey) and reduces it by 
        camera slack if either component is greater than slack
        """
        if abs(movex) > slack:
            pos_neg = 1 if movex > 0 else -1
            movex = pos_neg * (abs(movex) - slack)
        else: movex = 0
        if abs(movey) > slack:
            pos_neg = 1 if movey > 0 else -1
            movey = pos_neg * (abs(movey) - slack)
        else: movey = 0
        
        return movex, movey


    def stop_at_border(self):
        screen_w, screen_h = self.scene.game.draw_surface.get_size()

        # if background is too small then just return without modifying
        background_w, background_h = self.scene.bg_ref.rect.size
        if background_w < screen_w or background_h < screen_h:
            movex, movey = diff_vec(
                self.scene.bg_ref.sprite.rect.center,
                self.scene.game.get_center()
            )
            self.pan(movex, movey)
            return
    

        backx, backy = 0, 0
        if self.scene.bg_ref.rect.left > 0:
            backx = self.scene.bg_ref.rect.left
        elif self.scene.bg_ref.rect.right < screen_w:
            backx = self.scene.bg_ref.rect.right - screen_w

        if self.scene.bg_ref.rect.top > 0:
            backy = self.scene.bg_ref.rect.top
        elif self.scene.bg_ref.rect.bottom< screen_h:
            backy = self.scene.bg_ref.rect.bottom - screen_h

        self.pan(backx, backy)


    def center_player(self):
        tmp_storage = self.slack
        self.slack = 0
        self.follow_player()
        self.slack = tmp_storage


    def zoom_by(self, factor):
        if factor is None: return
        self.cur_zoom *= factor
        if self.cur_zoom == 0: self.cur_zoom = 1 # 0 resets scale
        background = self.scene.bg_ref
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        bg_w, bg_h = self.scene.bg_ref.rect.size
        bg_x, bg_y = self.scene.bg_ref.rect.topleft
        self.scene.bg_ref.scale_by(factor)
        bg_w_new, bg_h_new = self.scene.bg_ref.rect.size
        bg_x_new = centerx - bg_w_new * (centerx - bg_x) / bg_w
        bg_y_new = centery - bg_h_new * (centery - bg_y) / bg_h
        self.scene.bg_ref.rect.topleft = (bg_x_new, bg_y_new)

        for group in self.mobile_groups:
            if group == 'background': continue
            for sprite in self.scene.groups[group]:
                x, y = sprite.rect.center
                sprite.scale_by(factor)
                sprite.rect.center = (
                    bg_x_new + bg_w_new * (x - bg_x) / bg_w, 
                    bg_y_new + bg_h_new * (y - bg_y) / bg_h
                )   

    def zoom_abs(self, scale):
        self.zoom_by(0)
        self.zoom_by(scale)
