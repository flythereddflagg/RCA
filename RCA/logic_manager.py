# logic_manager.py
from constants import *


class LogicManager():
    
    def __init__(self, eng):
        self.eng         = eng
        self.all_sprites = self.eng.all_sprites
        self.background  = self.eng.background
        self.player      = self.eng.player
        self.spd_plr     = 5
        self.eslack      = CENTERX + CAMERASLACK
        self.wslack      = CENTERX - CAMERASLACK
        self.nslack      = CENTERY - CAMERASLACK
        self.sslack      = CENTERY + CAMERASLACK
        
    
    def logic(self):
        self.all_sprites.update()
        self.background.update()
    
    def left(self):
        if self.player.rect.x > self.wslack:
            self.player.rect.x -= self.spd_plr
        else:
            self.player.mv_background(self.spd_plr)
        self.player.walk_animate(W)
        
    def right(self):
        if self.player.rect.x < self.eslack:
            self.player.rect.x += self.spd_plr
        else:
            self.player.mv_background(self.spd_plr)
        self.player.walk_animate(E)
        
    def up(self):
        if self.player.rect.y > self.nslack:
            self.player.rect.y -= self.spd_plr
        else:
            self.player.mv_background(self.spd_plr)
        self.player.walk_animate(N)

    def down(self):
        if self.player.rect.y < self.sslack:
            self.player.rect.y += self.spd_plr
        else:
            self.player.mv_background(self.spd_plr)
        self.player.walk_animate(S)
    
    def no_key(self):
        self.player.stand()

