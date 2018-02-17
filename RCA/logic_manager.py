# logic_manager.py
from constants import *


class LogicManager():
    
    def __init__(self, eng):
        self.eng         = eng
        self.all_sprites = self.eng.all_sprites
        self.background  = self.eng.background
        self.player      = self.eng.player
    
    def logic(self):
        self.all_sprites.update()
    
    def left(self):
        if self.player.rect.x > WSLACK:
            self.player.rect.x -= PLAYERSPEED
        else:
            self.mv_cam(PLAYERSPEED, W)
        self.player.walk_animate(W)
        
    def right(self):
        if self.player.rect.x < ESLACK:
            self.player.rect.x += PLAYERSPEED
        else:
            self.mv_cam(PLAYERSPEED, E)
        self.player.walk_animate(E)
        
    def up(self):
        if self.player.rect.y > NSLACK:
            self.player.rect.y -= PLAYERSPEED
        else:
            self.mv_cam(PLAYERSPEED, N)
        self.player.walk_animate(N)

    def down(self):
        if self.player.rect.y < SSLACK:
            self.player.rect.y += PLAYERSPEED
        else:
            self.mv_cam(PLAYERSPEED, S)
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
        
        for i in self.eng.blocks.sprites():
            if   dr == N:
                i.rect.y += pixels
            elif dr == E:
                i.rect.x -= pixels
            elif dr == S:
                i.rect.y -= pixels
            elif dr == W:
                i.rect.x += pixels
    
    def cam_correct(self):
        if self.player.rect.x < WSLACK or\
                self.player.rect.x > ESLACK or\
                self.player.rect.y < NSLACK or\
                self.player.rect.y > SSLACK:
            if self.player.rect.y > SSLACK:
                self.player.rect.y -= PLAYERSPEED
                self.mv_cam(PLAYERSPEED,S)
            if self.player.rect.y < NSLACK:
                self.player.rect.y += PLAYERSPEED
                self.mv_cam(PLAYERSPEED,N)
            
            if self.player.rect.x > ESLACK:
                self.player.rect.x -= PLAYERSPEED
                self.mv_cam(PLAYERSPEED,E)
            if self.player.rect.x < WSLACK:
                self.player.rect.x += PLAYERSPEED
                self.mv_cam(PLAYERSPEED,W)

