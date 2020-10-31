# RCA package
# notice from copied code
import os
import json
from itertools import compress

import pygame as pg

# Screen Constants 
# Frame rate ( in Frames / second)
FPS          = 30 
# SCREENWIDTH  = 1300
# SCREENHEIGHT = 768
SCREENWIDTH  = 800
SCREENHEIGHT = 600
# screen size tuple
SCREENSIZE   = (SCREENWIDTH, SCREENHEIGHT)
# x and y coordinates for the center of the screen
CENTERX      = SCREENWIDTH  // 2 
CENTERY      = SCREENHEIGHT // 2 

# Animation Constants
# player speed in pixels / second
PLAYERPEEDTIME     = 300
# Player speed in pixels/frame
PLAYERSPEED         = PLAYERPEEDTIME // FPS
# image changes per minute
PLAYERANIMATERATE   = PLAYERPEEDTIME

# frames to next player animation
PLAYERANIMATEFRAMES = int(FPS * 60 / PLAYERANIMATERATE)

# pixels before camera moves instead of player
CAMERASLACK         = 100 
NSLACK              = CENTERY - CAMERASLACK
SSLACK              = CENTERY + CAMERASLACK
ESLACK              = CENTERX + CAMERASLACK
WSLACK              = CENTERX - CAMERASLACK

# direction constants North:0 East:1 South:2 West:3
DIRECTIONS      = list(range(4))
N,E,S,W         = DIRECTIONS
DIRECTION_DICT  = {"north": N, "east" : E, "south" : S, "west" : W}
INV_DIR_DICT     = {val:key for key, val in DIRECTION_DICT.items()}

# colors
BLACK           = (0,0,0)

COMMANDS = list(range(7))
UPDATE, LEFT, RIGHT, UP, DOWN, DO_A, DO_B = COMMANDS
KEY_MAPPING = {
    pg.K_u     : UPDATE,
    pg.K_LEFT  : LEFT,
    pg.K_RIGHT : RIGHT,
    pg.K_UP    : UP,
    pg.K_DOWN  : DOWN,
    pg.K_z     : DO_A,
    pg.K_x     : DO_B,
}

class DictObj(dict):
    """
    ******NOTICE***************
    optimize.py module by Travis E. Oliphant
    
    You may copy and use this module as you see fit with no
    guarantee implied provided you keep this notice in all copies.
    *****END NOTICE************
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '{\n' + '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])+"\n}"
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())

def get_data(path):
    path_ = path.replace("\\", "/")
    path_lst = path.split("/")
    path_len = len(path_lst)
    data = DictObj()

    for root, dirs, files in os.walk(path):
        root_ = root.replace("\\", "/")
        root_lst = root_.split("/")[path_len:]
        rt = data
        for branch in root_lst:
            rt = rt[branch]

        for dir_ in dirs:
            rt[dir_] = DictObj()
        
        rt.files = files
        for file_ in files:
            if file_.endswith(".json"):
                with open(root + "/" + file_, 'r') as f:
                    rt[file_[:-5]] = DictObj(**json.load(f))
        
    return data


def init_game(data_path):
    """
    this has to get all the necessary data or at least have a reference
    to it so all the necessary data can be found.
    """        
    pg.init()
    pg.display.set_caption("RCA")
    # Set up all sprite groups
    all_sprites = pg.sprite.Group() # everything
    background  = pg.sprite.Group() # background tiles
    foreground  = pg.sprite.Group() # non-interacting block
    block       = pg.sprite.Group() # non-moving sprites that interact
    player      = pg.sprite.Group() # sprites you can control             
    friend      = pg.sprite.Group() # moving friendly sprites
    foe         = pg.sprite.Group() # enemies
    hud         = pg.sprite.Group() # HUD (health, money etc.)
    misc        = pg.sprite.Group() # other (dialog boxes etc.)
    # set up groups list (in the order in which you want them to be drawn)
    groups = [background, foreground, block, player, friend, foe, hud, misc]

    # define groups that are diegetic (i.e. groups that exist in the game
    # world and will be affected by camera movement) EXCLUDES player
    diegetic_groups = [background, foreground, block, friend, foe]

    command_map = {
        UPDATE : update_zone,
        LEFT   : lambda g: direction_key(g, W),
        RIGHT  : lambda g: direction_key(g, E),
        UP     : lambda g: direction_key(g, N),
        DOWN   : lambda g: direction_key(g, S),
        DO_A   : action1,
        DO_B   : action2,
    }

    game = DictObj(
        data_path = data_path,
        data = get_data(data_path),
        clock = pg.time.Clock(),
        screen = pg.display.set_mode(SCREENSIZE),
        command_map = command_map,
        accept_input = True,
        keys_pressed = [],
        running = True,
        groups = groups,
        diegetic_groups = diegetic_groups,
        all_sprites = all_sprites,
        background = background,
        foreground = foreground,
        block = block,
        player = player,         
        friend = friend,
        foe = foe,
        hud = hud,
        misc = misc,
        events = [],
        on_keys = [],
        off_keys = [],
    )

    load_zone("zone1", game)
    
    return game

    
def engine(game):
    """
    Running this function will execute the initialized game.
    """
    
    while game.running:
        events(game)
        logic(game)
        draw(game)
        
        game.clock.tick(FPS)
    pg.quit()

    
def events(game):
    """
    Captures all events input by the user and updates the event variables
    """
    game.events = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running = False
            return
        game.events.append(event)

    new_keys = pg.key.get_pressed()
    if new_keys[pg.K_BACKSPACE]:
        game.running = False
        return

    # disregard numlock key
    if pg.K_NUMLOCK in new_keys: new_keys.remove(pg.K_NUMLOCK)
    
    old_keys = game.on_keys.copy()
    game.on_keys = list(compress(range(len(new_keys)), new_keys))
    game.off_keys = list(set(old_keys).difference(game.on_keys))


def logic(game):
    possible_keys = KEY_MAPPING.keys()
    for key in game.on_keys:
        if key in possible_keys:
            game.command_map[KEY_MAPPING[key]](game)
    
    reset_camera(game)
    game.all_sprites.update()

    
def draw(game):
    """
    Once the game logic method has run, this function updates all sprites
    based on what the logic method did and then draws the next frame in an
    order specified by the game manager.
    """
    game.screen.fill(BLACK)
    for group in game.groups:
        group.draw(game.screen)
    
    pg.display.flip()

        
def gen_sprite(path, scale=1):
    """Generates sprite with image file at path and scale"""
    sprite = pg.sprite.Sprite()
    sprite.image = pg.image.load(path).convert_alpha()
    width, height = sprite.image.get_size()
    width *= scale
    height *= scale
    sprite.image = pg.transform.scale(
        sprite.image,(int(width), int(height))
    )
    sprite.rect = sprite.image.get_rect()
    sprite.width = sprite.image.get_width()
    sprite.height = sprite.image.get_height()
    sprite.mask = pg.mask.from_surface(sprite.image)
    
    return sprite
    

def load_zone(zone_str, game, player_init=None):
    zone = game.data.sprites.zones[zone_str]
    assert zone.type == "zone"
    env = DictObj(**zone.environment)
    bg = gen_sprite(env.background)
    fg = gen_sprite(env.foreground)
    bg.rect.x, bg.rect.y = env.xy
    fg.rect.x, fg.rect.y = env.xy
    bg.add(game.all_sprites, game.background)
    fg.add(game.all_sprites, game.foreground)

    for block in zone.blocks:
        b = DictObj(**block)
        bsprite = gen_sprite(b.image_path)
        bsprite.rect.x, bsprite.rect.y = env.xy
        bsprite.add(game.all_sprites, game.block)

    if player_init is None:
        player = gen_sprite(
            "./data/sprites/player/larry_st_S.png",
            scale=3
        )
        player.rect.x, player.rect.y = CENTERX, CENTERY
        player.add(game.all_sprites, game.player)


def move(sprite, pixels, dr):
    if   dr == N:
        sprite.rect.y -= pixels
    elif dr == E:
        sprite.rect.x += pixels
    elif dr == S:
        sprite.rect.y += pixels
    elif dr == W:
        sprite.rect.x -= pixels


def move_camera(game, pixels, dr):
    for sprite in game.all_sprites:
        move(sprite, pixels, DIRECTIONS[dr - 2])



def reset_camera(game):
    px = game.player.sprites()[0].rect.x
    py = game.player.sprites()[0].rect.y
    bg = game.background.sprites()[0]
    bgxsize, bgysize = bg.image.get_width(), bg.image.get_height()
    
    cxerr, cyerr = px - CENTERX, py - CENTERY, 
    
    if abs(cxerr) > CAMERASLACK:
        movex =  int(cxerr - cxerr/abs(cxerr) * CAMERASLACK)
        move_camera(game, movex, E)
        # correct camera movement if you are at map edges
        if bg.rect.x + bgxsize < SCREENWIDTH or bg.rect.x > 0:
            for i in range(abs(movex)):
                move_camera(game, movex/abs(movex), W)
                if not (bg.rect.x + bgxsize < SCREENWIDTH or bg.rect.x > 0):
                    break

    if abs(cyerr) > CAMERASLACK:
        movey =  int(cyerr - cyerr/abs(cyerr) * CAMERASLACK)
        # correct camera movement if you are at map edges
        move_camera(game, movey, S)
        if bg.rect.y + bgysize < SCREENHEIGHT or bg.rect.y > 0:
            for i in range(abs(movey)):
                move_camera(game, movey/abs(movey), N)
                if not (bg.rect.y + bgysize < SCREENHEIGHT or bg.rect.y > 0):
                    break
        

def direction_key(game, dr):
    player = game.player.sprites()[0]
    fg = game.foreground
    check_collide = lambda p, fg: pg.sprite.spritecollide(
        p, fg, False, pg.sprite.collide_mask
    )

    move(player, PLAYERSPEED, dr)
    if check_collide(player, fg):
        for i in range(PLAYERSPEED):
            move(player, 1, DIRECTIONS[dr-2])
            reset_camera(game)
            if not check_collide(player, fg): 
                break

    # TODO add animation here
    # TODO add move rejection


def action1(game):
    print("action1")


def action2(game):
    print("action2")


def update_zone(game):
    print("update_zone")