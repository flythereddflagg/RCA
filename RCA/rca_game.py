"""
File     : rca_game.py
Author   : Mark Redd

"""
from constants import *
from player import Player
from zone1_json import Zone1
#from zone1 import Zone1


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
        self.players.add(self.player)
        self.all_sprites.add(self.player)        
        
        # Zone class will set up the blocks and background
        self.cur_zone = Zone1(self)


    def direction_key(self, direction):
        """
        Instruction set to complete when a direction key is pressed.
        Generally this will move the player.
        Takes @param direction
        """
        bool_vals = [
            self.player.rect.y > NSLACK,
            self.player.rect.x < ESLACK,
            self.player.rect.y < SSLACK,
            self.player.rect.x > WSLACK]

        if bool_vals[direction] or self.cur_zone.edge(direction):
            self.player.move(PLAYERSPEED, direction)
        else:
            self.mv_cam(PLAYERSPEED, direction)
        
        # if previous move was invalid undo move
        while bool(pg.sprite.spritecollide( 
                self.player, 
                self.foreground, 
                False,
                pg.sprite.collide_mask)):
            if bool_vals[direction-2] or\
                    self.cur_zone.edge(DIRECTIONS[direction-2]):
                self.player.move(1, DIRECTIONS[direction-2])
            else:
                self.mv_cam(1, DIRECTIONS[direction-2])            
         
        self.player.walk_animate(direction)

    
        
    def mv_cam(self, pixels, direction=None):
        """
        Moves the camera in @param 'direction' by moving everything but the
        player in the opposite direction.
        """
        if direction == None: direction = self.player.direction
        for sprite_group_obj in self.diegetic_groups:
            sprite_group = sprite_group_obj.sprites()
            for sprite in sprite_group:
                if   direction == N:
                    sprite.rect.y += pixels
                elif direction == E:
                    sprite.rect.x -= pixels
                elif direction == S:
                    sprite.rect.y -= pixels
                elif direction == W:
                    sprite.rect.x += pixels
    
    
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
        
        if   key == pg.K_u:
            self.cur_zone.update()
        elif key == pg.K_LEFT:
            self.direction_key(W)
        elif key == pg.K_RIGHT:
            self.direction_key(E)
        elif key == pg.K_UP:
            self.direction_key(N)
        elif key == pg.K_DOWN:
            self.direction_key(S)
    
    
    def no_key(self):
        self.player.stand()
    
    
    def logic(self):
        for blk in self.blocks.sprites():
            if pg.sprite.collide_rect(blk, self.player):
                blk.blk_do()
    
    
    def event_do(self, event):
        #print(event)
        pass

