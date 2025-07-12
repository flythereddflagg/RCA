import pygame as pg

from .tools import get_center_screen
from .node import Node

# TODO make adaptive camera the follows the player and gives them better FOV in the direction they are facing.

# TODO separate the zoom from screen size and zoom generally

class Camera(Node):
    def __init__(self, zoom=1, slack=0, **init):
        super().__init__(**init)
        self.mobile_groups = self.scene.draw_layers.copy()
        self.mobile_groups.remove('hud')
        self.cur_zoom = 1
        self.slack = slack
        self.zoom_by(self.scene.game.settings.SCALE * zoom)
        

    def update(self):
        player = self.scene.get_player()
        if not player:
            # if there is no player, 
            # move the camera to put the background topleft at 0,0
            background = self.scene.background.sprites()[0]
            movex, movey = background.sprite.rect.topleft
            self.pan(movex, movey)
            return
        self.follow_player()
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



    def follow_player(self):
        player = self.scene.get_player().sprite
        center = pg.math.Vector2(*get_center_screen())
        player_pos = pg.math.Vector2(player.rect.center)
        movex, movey = player_pos - center
        
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
        screen_w, screen_h = pg.display.get_surface().get_size()
        background = self.scene.background.sprites()[0]

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
        tmp_storage = self.slack
        self.slack = 0
        self.follow_player()
        self.slack = tmp_storage


    def zoom_by(self, factor):
        if factor is None: return
        self.cur_zoom *= factor
        if self.cur_zoom == 0: self.cur_zoom = 1 # 0 resets scale
        background = self.scene.background.sprites()[0]
        screen_data = pg.display.Info()
        centerx = screen_data.current_w // 2
        centery = screen_data.current_h // 2
        bg_w, bg_h = background.rect.size
        bg_x, bg_y = background.rect.topleft
        # background.scale_by(factor)
        bg_w_new, bg_h_new = background.rect.size
        bg_x_new = centerx - bg_w_new * (centerx - bg_x) / bg_w
        bg_y_new = centery - bg_h_new * (centery - bg_y) / bg_h
        background.rect.topleft = (bg_x_new, bg_y_new)

        for group in self.mobile_groups:
            if group == 'background': continue
            for sprite in self.scene.groups[group]:
                x, y = sprite.rect.center
                # sprite.scale_by(factor)
                sprite.rect.center = (
                    bg_x_new + bg_w_new * (x - bg_x) / bg_w, 
                    bg_y_new + bg_h_new * (y - bg_y) / bg_h
                )   

    def zoom_abs(self, scale):
        self.zoom_by(0)
        self.zoom_by(scale)
