"""
File     : rca_game.py
Author   : Mark Redd

"""
from constants import *
from player import Player
from zone import Zone


class RCAGame():
    """
    This class defines or refers to another class that defines all game logic.
    This class may be switched out for another game and used in it's place.
    """
    def __init__(self, eng):
        self.eng         = eng # get the engine

        # Set up all sprite groups
        self.all_sprites = pg.sprite.Group() # everything
        self.background  = pg.sprite.Group() # background tiles
        self.foreground  = pg.sprite.Group() # non-interacting blocks
        self.blocks      = pg.sprite.Group() # non-moving sprites that interact
        self.players     = pg.sprite.Group() # sprites you can control             
        self.friends     = pg.sprite.Group() # moving friendly sprites
        self.foes        = pg.sprite.Group() # enemies
        self.hud         = pg.sprite.Group() # HUD (health, money etc.)
        self.misc        = pg.sprite.Group() # other (dialog boxes etc.)
        
        # set up the groups list (this is the order in which you want them to 
        #   be drawn)
        self.groups_list = [
                            self.background,
                            self.foreground,
                            self.blocks    ,
                            self.players   ,
                            self.friends   ,
                            self.foes      ,
                            self.hud       ,
                            self.misc      ]
        # define groups that are diegetic (i.e. groups that exist in the game
        # world and will be affected by camera movement) EXCLUDES players
        self.diegetic_groups = [
                            self.background,
                            self.foreground,
                            self.blocks    ,
                            self.friends   ,
                            self.foes      ]
        # set up player
        self.player = Player(self)       
        
        # Zone class will set up the blocks and background
        self.current_zone = Zone(self, "zone1")
    
    
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
        # dictionary here?
        if   key == pg.K_u:
            self.current_zone.update()
        elif key == pg.K_LEFT:
            self.player.direction_key(W)
        elif key == pg.K_RIGHT:
            self.player.direction_key(E)
        elif key == pg.K_UP:
            self.player.direction_key(N)
        elif key == pg.K_DOWN:
            self.player.direction_key(S)
        elif key == pg.K_z:
            self.player.use_item_1()
        elif key == pg.K_x:
            self.player.use_item_2()
    
    
    def no_key(self):
        self.player.stand()
    
    
    def logic(self):
        for blk in self.blocks.sprites():
            if pg.sprite.collide_rect(blk, self.player):
                self.current_zone.blk_do(blk)
    
    
    def event_do(self, event):
        #print(event)
        pass

