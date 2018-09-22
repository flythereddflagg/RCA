"""
File     : player.py
Author   : Mark Redd

Player class. Should define all logic relating to the player.
"""
from constants import *
from rca_sprite import SpriteRCA
from item import Item

class Player(SpriteRCA):
    
    def __init__(self, game):
        super().__init__()
        self.img_paths = [
            "./sprites/player_sprite/larry_st_N.png",
            "./sprites/player_sprite/larry_wk_N.png",
            "./sprites/player_sprite/larry_st_S.png",
            "./sprites/player_sprite/larry_wk1_S.png",
            "./sprites/player_sprite/larry_wk2_S.png",
            "./sprites/player_sprite/larry_st_EW.png",
            "./sprites/player_sprite/larry_wk1_EW.png",
            "./sprites/player_sprite/larry_wk2_EW.png"]
        self.scale = 3
        self.images = (
            # stand, walk1, walk2
            (   self.gen_img(self.img_paths[0]),
                self.gen_img(self.img_paths[1]),
                pg.transform.flip(
                    self.gen_img(self.img_paths[1]), True, False)), # N
            
            (   self.gen_img(self.img_paths[5]),
                self.gen_img(self.img_paths[6]),
                self.gen_img(self.img_paths[7])), # E
            
            (   self.gen_img(self.img_paths[2]),
                self.gen_img(self.img_paths[3]),
                self.gen_img(self.img_paths[4])), # S
            
            (   pg.transform.flip(
                    self.gen_img(self.img_paths[5]), True, False),
                pg.transform.flip(
                    self.gen_img(self.img_paths[6]), True, False),
                pg.transform.flip(
                    self.gen_img(self.img_paths[7]), True,False))) # W

        self.game = game
        self.game.players.add(self)
        self.game.all_sprites.add(self) 
        self.direction = S
        self.image = self.images[self.direction][0]
        self.rect = self.image.get_rect()
        self.rect.x = CENTERX
        self.rect.y = CENTERY
        self.mask = pg.mask.from_surface(self.image)
        self.item = Item("./sprites/items/sword.png", self)
        self.counter = 0
        self.allow_move = True
        self.use_animate_bool = False
        self.allow_use_item = True


    def walk_animate(self, direction):
        self.direction = direction
        self.image = self.images[direction][1]\
            if self.counter < PLAYERANIMATEFRAMES / 2\
            else self.images[direction][2]
        self.counter += 1
        if self.counter > PLAYERANIMATEFRAMES: self.counter = 0 # reset counter
    

    def stand(self):
        self.image = self.images[self.direction][0]

        

    
    
    def move(self, pixels, dr=None):
        if dr == None: dr = self.direction
        if   dr == N:
            self.rect.y -= pixels
        elif dr == E:
            self.rect.x += pixels
        elif dr == S:
            self.rect.y += pixels
        elif dr == W:
            self.rect.x -= pixels

            
    def use_item_1(self):
        if not self.allow_use_item: return
        self.allow_move = False
        self.allow_use_item = False
        self.use_animate_bool = True
        self.game.players.add(self.item)
        self.game.all_sprites.add(self.item)
        self.image = self.gen_img("./sprites/player_sprite/larry_swing_E0.png")

    
    def use_item_2(self):
        print("Using item 2!")
        
        
    def direction_key(self, direction):
        """
        Instruction set to complete when a direction key is pressed.
        Generally this will move the player.
        Takes @param direction
        """
        if not self.allow_move: return
        bool_vals = [
            self.rect.y > NSLACK,
            self.rect.x < ESLACK,
            self.rect.y < SSLACK,
            self.rect.x > WSLACK]

        if bool_vals[direction] or self.game.current_zone.edge(direction):
            self.move(PLAYERSPEED, direction)
        else:
            self.mv_cam(PLAYERSPEED, direction)
        
        # if previous move was invalid undo move
        while bool(pg.sprite.spritecollide( 
                self, 
                self.game.foreground, 
                False,
                pg.sprite.collide_mask)):
            if bool_vals[direction-2] or\
                    self.game.current_zone.edge(DIRECTIONS[direction-2]):
                self.move(1, DIRECTIONS[direction-2])
            else:
                self.mv_cam(1, DIRECTIONS[direction-2])            
         
        self.walk_animate(direction)

        
    def mv_cam(self, pixels, direction=None):
        """
        Moves the camera in @param 'direction' by moving everything but the
        player in the opposite direction.
        """
        if direction == None: direction = self.direction
        for sprite_group_obj in self.game.diegetic_groups:
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
        