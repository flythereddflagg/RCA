# logic_manager.py
from constants import *


class LogicManager():
    
    def __init__(self, eng):
        self.eng         = eng
        self.all_sprites = self.eng.all_sprites
        #self.background  = self.eng.background
        #self.player      = self.eng.player
        self.accept_input = False
        '''
        # set up player
        self.player = Player(self)
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        
        # background set up
        self.bkgnd = Background(-1500,-1150)
        self.background.add(self.bkgnd)
        self.all_sprites.add(self.bkgnd)
        
        # Zone 1 class will set up the blocks
        self.zone1 = Zone1(self)
        '''
    
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
                False,
                pg.sprite.collide_mask)):
            ds = range(4)
            if bool_vals[direction-2]:
                self.mv_plr(PLAYERSPEED, ds[direction-2])
            else:
                self.mv_cam(PLAYERSPEED, ds[direction-2])
         
        self.player.walk_animate(direction)
    
    def no_key(self):
        pass
        #self.player.stand()
    
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
    
    def update_map(self):
        print("Updating Map...")
    
    def key_do(self, key):
        '''
        Runs a command corresponding to a 'key'. Where key is an integer
        that corresponds to a key press.
        Whenever called it checks if the key fed to it corresponds to a command.
        If it does, it runs that command.
        Before doing anything else it checks if the logic manager is accepting
        input. By default it accepts input. If 'self.accept_input' is set to 
        False, no keys are registered.
        '''
        if (not self.accept_input) or key == NOINPUTINDEX:
            return
        
        if   key == pg.K_u:
            self.eng.zone1.update()
        elif key == pg.K_LEFT:
            self.direction_key(W)
        elif key == pg.K_RIGHT:
            self.direction_key(E)
        elif key == pg.K_UP:
            self.direction_key(N)
        elif key == pg.K_DOWN:
            self.direction_key(S)
        elif key == pg.K_BACKSPACE:
            self.eng.running = False
        

