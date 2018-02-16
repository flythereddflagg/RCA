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
    
    def left(self):
        if self.player.rect.x > self.wslack:
            self.player.rect.x -= self.spd_plr
        else:
            self.mv_cam(self.spd_plr, W)
        self.player.walk_animate(W)
        
    def right(self):
        if self.player.rect.x < self.eslack:
            self.player.rect.x += self.spd_plr
        else:
            self.mv_cam(self.spd_plr, E)
        self.player.walk_animate(E)
        
    def up(self):
        if self.player.rect.y > self.nslack:
            self.player.rect.y -= self.spd_plr
        else:
            self.mv_cam(self.spd_plr, N)
        self.player.walk_animate(N)

    def down(self):
        if self.player.rect.y < self.sslack:
            self.player.rect.y += self.spd_plr
        else:
            self.mv_cam(self.spd_plr, S)
        self.player.walk_animate(S)
    
    def no_key(self):
        self.player.stand()
    
    def mv_cam(self,pixels, dr=None):
        if dr == None: dr = self.player.direction
        for i in self.eng.background.sprites():
            if   dr == N:
                i.rect.y += pixels
            elif dr == E:
                i.rect.x -= pixels
            elif dr == S:
                i.rect.y -= pixels
            elif dr == W:
                i.rect.x += pixels
    
    def cam_correct(self):
        if self.player.rect.x < self.wslack or\
                self.player.rect.x > self.eslack or\
                self.player.rect.y < self.nslack or\
                self.player.rect.y > self.sslack:
            if self.player.rect.y > self.sslack:
                self.player.rect.y -= self.spd_plr
                self.mv_cam(self.spd_plr,S)
            if self.player.rect.y < self.nslack:
                self.player.rect.y += self.spd_plr
                self.mv_cam(self.spd_plr,N)
            
            if self.player.rect.x > self.eslack:
                self.player.rect.x -= self.spd_plr
                self.mv_cam(self.spd_plr,E)
            if self.player.rect.x < self.wslack:
                self.player.rect.x += self.spd_plr
                self.mv_cam(self.spd_plr,W)

