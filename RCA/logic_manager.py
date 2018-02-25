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
    
    def direction_key(self, direction):
        bool_vals = [
            self.player.rect.y > NSLACK,
            self.player.rect.x < ESLACK,
            self.player.rect.y < SSLACK,
            self.player.rect.x > WSLACK
            ]
        
        if bool_vals[direction]:
            self.mv_plr(PLAYERSPEED, direction)
        else:
            self.mv_cam(PLAYERSPEED, direction)
        # if previous move was invalid undo move
        if bool(pg.sprite.spritecollide( 
                self.player, 
                self.eng.blocks, 
                False)):
            ds = range(4)
            if bool_vals[direction-2]:
                self.mv_plr(PLAYERSPEED, ds[direction-2])
            else:
                self.mv_cam(PLAYERSPEED, ds[direction-2])
         
        self.player.walk_animate(direction)
    
    def no_key(self):
        self.player.stand()
    
    def mv_cam(self, pixels, dr=None):
        if dr == None: dr = self.player.direction
        for j in [
                self.eng.background.sprites(),
                self.eng.blocks.sprites(),
                self.eng.friends.sprites(),
                self.eng.foes.sprites()]:
            for i in j:
                self.cam_sprite(dr, i, pixels)
    
    def cam_sprite(self, dr, i, pixels):
        if   dr == N:
            i.rect.y += pixels
        elif dr == E:
            i.rect.x -= pixels
        elif dr == S:
            i.rect.y -= pixels
        elif dr == W:
            i.rect.x += pixels
    
    def mv_plr(self, pixels, dr=None):
        if dr == None: dr = self.player.direction
        if   dr == N:
            self.player.rect.y -= pixels
        elif dr == E:
            self.player.rect.x += pixels
        elif dr == S:
            self.player.rect.y += pixels
        elif dr == W:
            self.player.rect.x -= pixels
    
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

