"""
RCA_w1_v0-2beta.py
Red Castle Avenger
World1: In the Shadow of the Mountain
version: 0.2 beta

Programmed by: Mark Redd <flythereddflagg>
Story by: Mark Redd
For bugs and fixes: email <redddogjr@gmail.com>

Fixes to this version include:
    - stripping down unneeded imports
    - implementing a 'save game' option
    - fixing minor gramatical errors
"""
from string import maketrans, punctuation
from Tkinter import Tk, Canvas, Frame, BOTH, NW, END, StringVar,\
    Entry, Label, LEFT
from PIL import ImageTk, Image
from random import randint as rnt, choice
from pickle import dump, load

class Engine():
    #gives output --> gets input from user --> processes input *loops
    end_list = [
    'game_over',
    'game over 1',
    'game over 2',
    'game_over_win'
    ]

    def __init__(self, parser, player):
        self.parser = parser
        self.player = player
        self.gm_ovr = False

    def play(self):
        out1 = None
        input1 = 'look'
        while True:
            out1, pos = self.process_inp(input1)
            self.outp(out1)
            input1 = self.gets_inp()
                
    def outp(self, out):
        print out
    
    def gets_inp(self):
        com = raw_input("> ")
        return com
    
    def process_inp(self, inputs):
        """returns which text to get"""

        if self.gm_ovr == True:
            end_it = "-- GAME OVER --\n   press Escape to exit..."
            out = "%s" % end_it
            return out, 'game_over'

        inputs = self.parser.sim_words(inputs)
        if 'save' in inputs or 'load' in inputs:
            return inputs, 'game state'
        out = self.player.outpp(inputs)
        pos = self.player.get_pos()
        
        if out == 'game_over_win':
            pos = 'win1'
        
        if not isinstance(out, basestring) and 'game_over' in out:
            self.gm_ovr = True
            out = self.game_over(out[0], out[1])
        elif out in self.end_list:
            self.gm_ovr = True
            out = self.game_over(out)
            
        return out, pos

    def game_over(self, out=None, out_die=None):
        if out == 'game over 1':
            out = Pos1_man().look4
        elif out == 'game_over':
            out_over = Place().look_dead
            out = '%s\n%s' % (out_die, out_over)
        elif out == 'game over 2':
            out = Pos1_man().look5
        elif out == 'game_over_win':
            out = Pos1_man2_4().look_win_world1
        return out

        
class Parser():

    commands = {
# The following is the game lexicon. All words in this lexicon will
# be recognized by the parser and processed.
#   <directions: commands with feet>
        'g':'go','go':'go','walk':'go','enter':'go',
            'crawl':'go','run':'go',
        'up':'up', 'u':'up',
        'down':'down','d':'down',
        'north':'north','n':'north',
        'south':'south','s':'south',
        'east':'east','e':'east',
        'west':'west','w':'west',
#   <commands with hands>
        'get':'get','gt':'get','take':'get','grab':'get','steal':'get',
            'obtain':'get',
        'drop':'drop','d':'drop','put':'drop',
        'use':'use','utilize':'use','give':'use',
#   <special or one-time use commands>
        'hide':'hide',
        'fight':'fight',
        'flee':'flee',
        'cut':'cut',
        'climb':'climb',
        'throw':'throw',
#   <battle commands>
        'punch':'punch',
        'swing':'swing',
        'stab':'stab',
        'defend':'defend',
        'evade':'evade',
        'dodge':'evade',
#   <other commands>
        'talk':'talk',
        'inventory':'inventory','inv':'inventory',
        'equip':'equip','eq':'equip',
        'unequip':'unequip','uneq':'unequip',
        'look':'look','l':'look',
        'map': 'map',
        'save':'save',
        'load':'load',
#   <items>
        'bigkey':'bigkey',
        'sword':'sword',
        'shovel':'shovel',
        'pickle':'pickle',
        'key': 'key',
#   <cheat commands>
        'warp': 'warp',
        '1' : 1,
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        '0' : 0,
        'superget':'superget'
    }

    def sim_words(self, words):
    
        words = words.lower()
        words = words.translate(maketrans("",""), punctuation)
        words = words.split()
        
        err = []
        for n,i in enumerate(words):
            try:
                i = self.commands[i]
                words[n] = i
            except KeyError:
                err.append(words[n])
        for i in err:
            if i in words:
                words.remove(i)        
        if words == []:
            words = "\nI don't understand that\n"
        return words


class Place():

    battle = False
    blocked  = False
    i_consume = False
    special_get = False
    incrementer = 0
    crdnts = None
    items = []
    enemy_spawn = True
    
    battle_list = [
        'battle goblin',
        'battle darkwolf'
        ]
    
    look1 = "\n\nThis space has nothing in it yet. You had best go back...\n\n"    
    look_dead = """
Sorry, you died...
-- GAME OVER --
press Escape to exit...
"""
        
    def item_here(self):
        if self.items == []:
            return ""
        else:
            item_here = '\n'.join(self.items)
            here_stuff =  "\nThings that are here:\n%s" % item_here
            return here_stuff
            
    def chances(self, den):
        y = rnt(1,den)
        x = den/2
        if y == x:
            return True
        else:
            return False 
 
    def look(self):
        if self.chances(7) == True and self.enemy_spawn == True:
            btl = choice(self.battle_list)
            self.enemy_spawn = False
            return btl
        
        self.enemy_spawn = False
        
        if not isinstance(self.look1, basestring):
            return self.look1
        else:
            return "%s\n%s %s" % (self.crdnts, self.look1,\
                self.item_here())
    
    def use(self, inp):
        return "You can't use that here."
    
    def get(self, inp):
        pass
    
    def talk(self, inp):
        return "There's no one to talk to."
    
    def fight(self, inp):
        return "You can't do that here."
        
    def flee(self, inp):
        return "You can't do that here."
        
    def hide(self, inp):
        return "There's nowhere to hide."
    
    def cut(self, inp):
        return "You can't do that here."
        
    def climb(self, inp):
        return "You can't do that here."
        
    def throw(self, inp):
        return "You can't do that here."

class Item():
    name = "Unknown Item"
    damage_multiplier = 0
    defense = 0

class BigKey(Item):
    name = "bigkey"

class Key(Item):
    name = "key"

class Pickle(Item):
    name = "pickle"

class Sword(Item):
    name = "sword"
    damage_multiplier = 1
    defense = 2

class Shovel(Item):
    name = "shovel"
    damage_multiplier = .5
    defense = 3

    
class Player1():
    def __init__(self, position, map, enemy=None):
        self.map = map
        self.position = position
        self.inventory = []
        self.weapon1 = None
        self.health = 100
        self.enemy = enemy
        self.battle = False

    options = """You can PUNCH or EVADE your enemy or if you have equipped an item with EQUIP [item] 
you can SWING, CUT, STAB or DEFEND with it."""

    game_items = [
        'bigkey',
        'sword',
        'shovel',
        'pickle',
        'key'
        ]
    
    game_objects = {
        'bigkey': BigKey(),
        'sword' : Sword(),
        'shovel': Shovel(),
        'pickle': Pickle(),
        'key'   : Key()
        }
    
    battle_commands = [
        'punch',
        'swing',
        'stab'
        ]

    p_react_list = [
        'change map--1.1',
        'change pos--4,3',
        'change pos--7,1',
        'battle -50 hp dragon',
        'battle dragon',
        'battle goblin',
        'battle darkwolf'
        ]

    def get_pos(self):
        try:
            out =  self.position.crdnts
        except:
            out = "This is a problem you need ot fix on line 239 ish"
        return out
    

    def inv_show(self):
        if self.inventory == []:
            show_inv =  "Inventory is empty."
        else:
            inv = '\n'.join(self.inventory)
            show_inv = 'INVENTORY:\n%s' % inv
            if self.weapon1 != None:    
                equip = "Equipped Item:\n%s" % self.weapon1.name
                show_inv = "%s\n%s" % (equip, show_inv)
        
        show_inv = "Player hp: %s\n%s" % (self.health, show_inv)
        return show_inv
    
    def get(self, inp):
        for i in inp:
            if i in self.position.items:
                self.inventory.append(i)
                self.position.items.remove(i) 
                if self.position.special_get == True:
                    return self.position.get(inp)
                else:
                    return "Taken."
        return "I don't see that here."
    
    def drop(self,inp):
        for i in inp:
            if i in self.inventory:
                self.inventory.remove(i) 
                self.position.items.append(i)
                if i in self.equipped_item:
                    self.equipped_item = []
                return "Dropped."

        return "\nItem not found in inventory.\n"
        
    def equip(self,inp):
        for i in inp:
            if i in self.inventory:
                self.weapon1 = self.game_objects[i]
                return "%s equipped" % i
                
        return "Item not found in inventory."
         
    def unequip(self,inp):
        for i in inp:
            if i in self.inventory:
                self.equipped_item = []
                return "%s unequipped" % i
                
        return "You don't have that item."
    
    def look(self):
        return self.position.look()
    
    def use(self, inp):
        for i in inp:
            if i in self.game_items:
                if i in self.inventory:
                    if self.position.i_consume == True:
                        out, i = self.position.use(inp)
                        self.inventory.remove(i)
                    else:
                        out = self.position.use(inp)
                    return out
                else:
                    return "You don't have that item."

        return "I've never heard of that item."

    def use_fight(self, weapon):
        if weapon == None:
            out = "You must equip an item before you can do that."
        else:
            out = self.enemy.use_fight(weapon)
        return out

    def talk(self, inp):
        return self.position.talk(inp)
        
    def go(self, inp):
        last_pos = self.position
        
        if self.position.blocked == True:
            self.position = self.position.go(inp)
            if self.position == "\nYou can't go that way.\n":
                self.position = last_pos
                return "\nYou can't go that way.\n"
            else:
                self.position = last_pos

        if 'east' in inp:
            self.position = self.map.pos(self.position.crdnts\
                [0], self.position.crdnts[1] + 1)
        elif 'west' in inp:
            self.position = self.map.pos(self.position.crdnts\
                [0], self.position.crdnts[1] - 1)
        elif 'north' in inp:
            self.position = self.map.pos(self.position.crdnts\
                [0] - 1, self.position.crdnts[1])
        elif 'south' in inp:
            self.position = self.map.pos(self.position.crdnts\
                [0] + 1, self.position.crdnts[1])
        else:
            return "\nWhat direction is that?\n"
        
        if self.position == "\nYou can't go that way.\n":
            self.position = last_pos
            return "\nYou can't go that way.\n"
        
        return self.look()
        
    def warp(self, inp):
        try:
            self.position = self.map.pos(inp[1], inp[2])
            return self.look()
        except:
            return "Looks like you can't even cheat correctly."
            
    def superget(self, inp):
        for i in inp:
            if i in self.game_items:
                self.inventory.append(i)
                return "You got it!"
        return "I've never heard of that item."    
    
    def battle_start(self):
        self.battle = True
        self.return_to_pos = self.position
        self.position = Battle(self.enemy)
        out = self.enemy.start()
        out = "Player hp:%s, %s hp:%s\n\n%s\n\n%s" % (self.health,\
            self.enemy.name, self.enemy.hp, out, self.options)
        return out
        
    def battle_win(self):
        self.battle = False
        self.position = self.return_to_pos
    
    def outpp(self, inp):
        if self.battle == True:
            return self.outpp_battle(inp)
        
        if inp == "\nI don't understand that\n":
            out = inp
        elif 'inventory' in inp:
            out = self.inv_show()
        elif 'equip' in inp:
            out = self.equip(inp)
        elif 'unequip' in inp:
            out = self.unequip(inp)
        elif 'get' in inp:
            out = self.get(inp)
        elif 'drop' in inp:
            out = self.drop(inp)
        elif 'look' in inp:
            out = self.look()
        elif 'go' in inp:
            out = self.go(inp)
        elif 'use' in inp:
            out = self.use(inp)
        elif 'talk' in inp:
            out = self.talk(inp)
        elif 'warp' in inp:
            out = self.warp(inp)
        elif 'superget' in inp:
            out = self.superget(inp)
        elif 'map' in inp:
            out = 'MAP'
        elif 'fight' in inp:
            out = self.position.fight(inp)
        elif 'hide' in inp:
            out = self.position.hide(inp)
        elif 'flee' in inp:
            out = self.position.flee(inp)
        elif 'cut' in inp:
            if 'sword' in self.inventory:
                out = self.position.cut(inp)
            else:
                out = "You'll need a sword to do that."
        elif 'climb' in inp:
            out = self.position.climb(inp)
        elif 'throw' in inp:
            if 'sword' in self.inventory:
                out = self.position.throw(inp)
            else:
                out = "You'll need a sword to do that."
        else:
            out = "I don't understand that."
        
        if out in self.p_react_list:
            out = self.player_react(out)

        return out

    def player_react(self,out):          
        if out == 'change map--1.1':
            self.map = Map1_1()
            self.position = Pos1_man3_3()
            out = self.position.look2
        elif out == 'change pos--4,3':
            self.position = Pos1_4_3()
            out = self.position.look2
        elif out == 'change pos--7,1':
            self.position = Pos1_man()
            out = self.position.look1
        elif out  == 'battle -50 hp dragon':
            self.enemy = Dragon(hp=50, advantage=True)
            out = self.battle_start()
        elif out == 'battle dragon':
            self.enemy = Dragon()
            out = self.battle_start()
        elif out == 'battle goblin':
            self.enemy = Goblin()
            out = self.battle_start()
        elif out == 'battle darkwolf':
            self.enemy = DarkWolf()
            out = self.battle_start()
        return out

    def outpp_battle(self, inp):
        weapon = self.weapon1
        hrt = 0
        
        if inp == "\nI don't understand that\n":
            out = inp
        elif 'inventory' in inp:
            out = self.inv_show()
        elif 'equip' in inp:
            out = self.equip(inp)
        elif 'unequip' in inp:
            out = self.unequip(inp)
        elif 'get' in inp:
            out = self.get(inp)
        elif 'drop' in inp:
            out = self.drop(inp)
        elif 'look' in inp:
            out = self.enemy.look()
        elif 'talk' in inp:
            out = self.talk(inp)
        elif 'hide' in inp:
            out = self.position.hide(inp)
        elif 'flee' in inp:
            out = self.enemy.flee(inp)
        elif 'use' in inp:
            out, hrt = self.enemy.foe_react('swing', weapon)
        elif 'fight' in inp:
            out, hrt = self.enemy.foe_react('swing', weapon)
        elif 'punch' in inp:
            out, hrt = self.enemy.foe_react('punch')
        elif 'swing' in inp:
            out, hrt = self.enemy.foe_react('swing', weapon)
        elif 'cut' in inp:
            out, hrt = self.enemy.foe_react('cut', weapon)
        elif 'stab' in inp:
            out, hrt = self.enemy.foe_react('stab', weapon)
        elif 'defend' in inp:
            out, hrt = self.enemy.foe_react('defend', weapon)
        elif 'evade' in inp:
            out, hrt = self.enemy.foe_react('evade', weapon)
        else:
            out = "I don't understand that. Are you using battle commands?"
        
        if hrt == 'win':
            self.battle_win()
            return out
        elif hrt == 'win_world1':
            self.battle = False
            out = 'game_over_win'
            return out
            
        if out in self.p_react_list:
            out = self.player_react(out)
            
        self.health = self.health - hrt
        
        if self.health > 0:
            out = "Player hp:%s, %s hp:%s\n\n%s\n\n%s" % (self.health,\
                self.enemy.name, self.enemy.hp, out, self.options)
        else:
            out_die = "Player hp:%s, %s hp:%s\n\n%s" % (self.health,\
                self.enemy.name, self.enemy.hp, out)
            out_over = 'game_over'
            out = [out_over, out_die]
            
        return out
        
class Battle(Place):
    battle = True
    crdnts = 'battle'
    
    look1 = "You are in the middle of a battle! This is no time to be sight seeing!"
    
    def __init__(self, opponent):
        self.opponent = opponent
        
    def look(self):
        return self.look1


class Foe():
    name = "Foe!"
    look1 = ""
    
    def __init__(self):
        self.hp = 100


    start1 = "This is a new foe! There's nothing to fight yet..."
    def look(self):
        return self.look1
    
    def chances(self, den):
        y = rnt(1,den)
        x = den/2
        if y == x:
            return True
        else:
            return False
    
    def start(self):
        return self.start1
    
    damages = {
        'punch': 10,
        'swing': 15,
        'cut'  : 25,
        'stab' : 50
        }
    
    def defeated(self):
        return "The enemy is defeated.", 'win'
        
    def strike(self):
        out = "The enemy strikes!"
        hrt = 10
        return out, hrt
    
    def slash(self):
        out = "The enemy slashes!"
        hrt = 20
        return out, hrt
        
    def bide(self):
        out = "The enemy bides!"
        hrt = 0
        return out, hrt
        
    def foe_attack(self):
        
        a = self.strike()
        b = self.slash()
        c = self.bide()
        
        x = [a, b, c]
        attack = choice(x)
        
        return attack[0], attack[1]


    def foe_react(self, move, weapon=None):
    
        dmg = -1
        dfnd = None
        hrt = None
        evd = False
        result_player = ""
        result_foe = ""
        
        if weapon == None:
            mlt = 0
        else:
            mlt = weapon.damage_multiplier
        
        if   move == 'punch':
            dmg = self.damages['punch']
            result_player = "You punch your foe!"
        elif move == 'swing'  and weapon != None:
            dmg = self.damages['swing']* mlt
            result_player = "You swing your weapon!"
        elif move == 'cut'    and weapon != None:
            dmg = self.damages['cut']  * mlt
            result_player = "You cut with your weapon!"
        elif move == 'stab'   and weapon != None:
            dmg = self.damages['stab'] * mlt
            result_player = "You stab at your foe!"
        elif move == 'defend' and weapon != None:
            dfnd = weapon.defense
            result_player = "You defend with your weapon!"
        elif move == 'evade':
            evd = True
            result_player = "You evade!"
        else:
            result_player =  "You have no weapon in hand! You must EQUIP a weapon!"
        
        missed = self.chances(25)
        if missed == True and dfnd == None and evd == False:
            dmg = 0
            miss_msg = "You missed!"
        else:
            miss_msg = ""
        
        if dmg == 0:
            result_player = "Your attack had no effect!"
        elif dfnd == 0:
            result_player = "You are unable to defend yourself with your weapon!"
        
        result_foe, hrt = self.foe_attack()
        
        if dfnd != 0 and dfnd != None:
            hrt = hrt - hrt*1.0/hrt
        
        if evd == True:
            missed_player = self.chances(2)
            if missed_player == True:
                hrt = 0
                miss_msg = "Enemy missed you!"
        
        if dmg == -1:
            dmg = 0
        
        if hrt == None:
            hrt = 0
        
        self.hp = self.hp - int(dmg)
        
        if self.hp <= 0:
            x = self.defeated()
            return x[0], x[1]
            
        dmg = int(dmg)
        hrt = int(hrt)
        
        out = "%s %s\n%s\nEnemy took %s damage, You took %s damage."\
            % (result_player, miss_msg, result_foe, dmg, hrt)

        self.look1 = out

        return out, hrt

class Goblin(Foe):
    
    def __init__(self):
        self.hp = 15
    
    name = 'Goblin'
    start1 = "Suddenly a Goblin jumps out and attacks!"
    
    def strike(self):
        out = "The Goblin strikes you with his club!"
        hrt = 5
        return out, hrt
    
    def slash(self):
        out = "The Goblin slashes at you with his claws!"
        hrt = 10
        return out, hrt
        
    def bide(self):
        out = "The Goblin is preparing to attack!"
        hrt = 0
        return out, hrt
    
    def defeated(self):
        return "The Goblin, now defeated, bursts into flame and disappears...", 'win'

class DarkWolf(Foe):
    
    def __init__(self):
        self.hp = 25
    
    name = 'Dark Wolf'
    start1 = "Suddenly a Dark Wolf jumps out and attacks!"
    
    def strike(self):
        out = "The Dark Wolf bites you!"
        hrt = 20
        return out, hrt
    
    def slash(self):
        out = "The Dark Wolf slashes at you with his claws!"
        hrt = 5
        return out, hrt
        
    def bide(self):
        out = "The Dark Wolf lets out a blood-curdling howl!"
        hrt = 0
        return out, hrt
    
    def defeated(self):
        return "The Dark Wolf, now defeated, bursts into flame and disappears...", 'win'
        
class Dragon(Foe):

    name = 'Dragon'

    start_ad = """The chandelier falls right over the Dragon's head and you see opportuinty looming.
You take a leap forward off the balcony on to the Dragon's back and thrust your sword as hard as you
can into his side. The Dragon shrieks and throws you to the side. You catch yourself in a roll and
find yourself facing the Dragon. The dragon is momentarily stunned from the chandelier. 

You have a chance to land the first blow! What do you do? """
    
    start1 = """You swing out onto the chandelier and grab hold. As you jump on, the ceiling gives 
way and comes crashing down upon you and the dragon. You land on the dragon's head but with a little 
toss he throws you off. Turns out that dragon was a little faster than you expected. He dodges the 
falling debris as you roll away. Well that didn't pan out.

The dragon is momentarily distracted with the debris. You have a chance to land the first blow! What do you do?"""

    def __init__(self, hp=100, advantage=False):
        self.hp = hp
        self.advantage = advantage
    
    def start(self):
        if self.advantage == True:
            return self.start_ad
        else:
            return self.start1
    
    def strike(self):
        out = "The Dragon swings his spiked tail at you!"
        hrt = 30
        return out, hrt
    
    def slash(self):
        out = "The Dragon slashes at you with his claws!"
        hrt = 20
        return out, hrt
        
    def bide(self):
        out = "The Dragon's eyes blaze as he prepares to attack!"
        hrt = 0
        return out, hrt
        
    def fireball(self):
        out = "The Dragon unleashes a fireball at you!"
        hrt = 50
        return out, hrt

    def defeated(self):
        return "The enemy is defeated.", 'win_world1'
        
    def foe_attack(self):
        
        a = self.strike()
        b = self.slash()
        c = self.bide()
        d = self.fireball()
        
        x = [a, b, c, a, b, c, d]
        attack = choice(x)
        
        return attack[0], attack[1]
        
        
###############################################################################    
#                          WORLD 1 MAP SECTION                                #
###############################################################################

class Pos1_1_1(Place):
    look1 = """
You come to the end of the corridor where what must have been the servant's
entrance is destroyed and blocked off. There appears to be nothing but rubble
here.
"""
    look2 = """
You dig through the rubble and unearth the fabled normal, regular, 
boring KEY! YEAH! Now we're getting somewhere!
"""	
    look3 = """
You already got the key. Move on.
"""
    look4 = """
You made a mess looking for that key. This would be a problem except
this area is already wrecked so things don't look all that different.
There is most definitely nothing but rubble here now.
"""
    def look(self):
        if self.hole_dug == True:
            here = self.look4
        elif self.hole_dug == False:
            here = self.look1
    
        return "%s\n%s %s" % (self.crdnts, here, self.item_here())

    def use(self, inp):
        if self.hole_dug == True:
            return self.look3
        elif 'shovel' in inp:
            self.hole_dug = True
            self.items.append('key')
            return self.look2
        else:
            return "That item does you no good here."
            
    hole_dug = False
    crdnts = [1, 1]
    items = []



class Pos1_1_2(Place):

    look1 = """You are at the bottom of the stairs. You are shocked to find a human
at the bottom of the stairs! The poor man appears to have
been crushed with a blunt object because all of the ribs on one side
are broken.
The path continues EAST and WEST.
"""
    crdnts = [1, 2]
    items = []



class Pos1_1_3(Place):

    look1 = """
The high fence is replaced by brick wall here. The narrow passage is
dark and covered. A narrow passage leads down some stairs. The only
options are to proceed EAST or WEST.
"""
    crdnts = [1, 3]
    items = []



class Pos1_1_4(Place):

    look1 = """
Now behind the mansion you can see that this narrow passage was
apparently used by servants that worked at the mansion as an entrance.
The path runs EAST and WEST and is quite dim and dreary.
"""
    crdnts = [1, 4]
    items = []



class Pos1_1_5(Place):

    look1 = """
You are standing at the North east corner of the grounds of the
mansion. There is a high fence around the perimeter of the mansion.
You look WEST and see a narrow passage between the dense trees and
the high fence. It is just wide enough to allow one person to walk
through comfortably.
"""
    crdnts = [1, 5]
    items = []



class Pos1_2_5(Place):

    look1 = """You are standing on the east side of the grounds of the mansion.
There is a high fence around the perimeter of the mansion that looks
unclimable.
"""
    crdnts = [2, 5]
    items = []



class Pos1_2_6(Place):
    enemy_spawn = False
    look1 = """
You are at the north end of the garden. In front of you is a marble
statue of a tall cruel-looking man in fine clothing. In his hand he
holds a chain that is wrapped around his hands and neck. Part of the
chain is resting at his feet. On the end of the chain is a large LOCK
that apparently is binding this man to the ground. On the statue is 
the inscription: "I wear the chain I forged in life. Now, in death, I
seek him who..." A chunk is missing out of the stone and the message
ends there.
"""
    def use(self, inp):
        if 'key' in inp:
            return 'change pos--7,1'
        else:
            return "That item does you no good here."

    crdnts = [2, 6]
    items = []



class Pos1_3_5(Place):

    look1 = """You are standing on the east side of the grounds of the mansion.
There is a high fence around the perimeter of the mansion that looks
unclimable. Through the high fence you can see the well kept grounds
and ostentatious gargoyles carved into the sides of the mansion.
"""
    crdnts = [3, 5]
    items = []



class Pos1_3_6(Place):

    look1 = """You are standing in a neat garden which runs NORTH and SOUTH. Neatly
planted trees span the garden and beautifully kept hedges line the
sides. You are careful not to step on any of the plants though you
are not sure why.
"""
    crdnts = [3, 6]
    items = []



class Pos1_3_7(Place):

    look1 = """You are in a clearing with dense forest to the north and east. To the
WEST you see a large mansion.
"""
    crdnts = [3, 7]
    items = []



class Pos1_4_2(Place):

    look1 = """Here the trees have over grown the high fence. It is impossible to go
around the mansion this way. And with the river to the south the only
way to go is back to the EAST.
"""
    crdnts = [4, 2]
    items = ['shovel']



class Pos1_4_3(Place):

    look1 = """You are standing in front of the large gate to the mansion. There is a
lock here that secures the gate shut.
"""
    look2 = """
Following good sense. You flee and find your way out of the mansion
through the front door. You sprint across the grounds and find a ladder
that is laid against the fence. You scale this and jump over finding
yourself on the other side by the front gate of the mansion.
The dragon apparently did not notice you there because he isn't pursuing
you. You look around.
"""
    crdnts = [4, 3]
    items = []



class Pos1_4_4(Place):

    look1 = """You are on a driveway between the river and the high fence surrounding
the mansion. Through the high fence you can see the well kept grounds
and ostentatious gargoyles carved into the sides of the mansion.
"""
    crdnts = [4, 4]
    items = []



class Pos1_4_5(Place):

    look1 = """
You are standing at the south east corner of the grounds of the
mansion. There is a high fence around the perimeter of the mansion.
You look WEST and see the front gate faces south and the road to it
runs along the north bank of the river.
"""
    crdnts = [4, 5]
    items = []



class Pos1_4_6(Place):

    look1 = """
You are standing in a neat garden which runs NORTH and south
and ends at the river near where you are standing. Neatly
planted trees span the garden and beautifully kept hedges line the
sides. You are careful not to step on any of the plants though you
are not sure why.
"""
    crdnts = [4, 6]
    items = []



class Pos1_4_7(Place):

    look1 = """
You are at the north end of a bridge that crosses the river. You can
cross the bridge by proceeding SOUTH. You see in the distance to the
WEST a large mansion. To the NORTH and east you see a large forest
which is thick and dark.
"""
    crdnts = [4, 7]
    items = []



class Pos1_5_7(Place):

    look1 = """
You are standing in the middle of the bridge. From here you can see a
large mansion to the Northwest. Your only options here are to go to
the NORTH side of the river or the SOUTH side. There is little else
here."""
    crdnts = [5, 7]
    items = []



class Pos1_6_4(Place):

    enemy_spawn = False
    
    look1 = """
You are at the end of the corridor of trees. To the EAST there is a 
tall wooden gate that is chained shut. If you had the BIGKEY you could
unlock the large padlock that holds the chain taut.
"""
    look2 = """
You are at the end of the corridor of trees. There is a 
tall wooden gate standing open revealing a passage to the EAST. 
To the SOUTH lies a dim corridor of trees.
"""
    look3 = """
You insert the BIGKEY into the lock...
With some effort, the key turns and the lock falls off
the chain. You pull the wooden gate open revealing a
Passage to the EAST.
"""
    
    def look(self):
        if self.door_open == True:
            here = self.look2
        elif self.door_open == False:
            here = self.look1
    
        return "%s\n%s %s" % (self.crdnts, here, self.item_here())

    def use(self, inp):
        if self.door_open == True:
            return "The gate is already open."
        elif 'bigkey' in inp:
            self.door_open = True
            return self.look3
        else:
            return "That item does you no good here."
    
    door_open = False
    crdnts = [6, 4]
    items = ['pickle']



class Pos1_6_5(Place):
    
    enemy_spawn = False
    
    look1 = """
You find yourself in a small clearing in the dense woods. In the middle
of the clearing is a long and brilliantly polished SWORD laying upon a
stone table. The sun shines down and illuminates the clearing with the
sword's refection.
The only way out is back to the WEST.
"""
    look2 = """
You find yourself in a small clearing, dimly lit from the small shaft of
sunlight that breaks through the trees. In the middle of the clearing is
a stone table about waist height. For lack of lighting you can see 
little else in the clearing.
The only way out is back to the WEST.
"""
    look3 = """ 
As you take the sword in your hand you feel strength flow through you.
The sword's polished surface, once removed from the stone table, stops 
illuminating the clearing. The clearing is dim now. You have taken the 
sword's power into yourself. You are now ready to face the evil that 
awaits...
"""
    crdnts = [6, 5]
    items = ['sword']
    special_get = True
    
    def look(self):
        if 'sword' in self.items:
            here = self.look1
        else:
            here = self.look2
    
        return "%s\n%s %s" % (self.crdnts, here, self.item_here())
    
    def get(self, inp):
        if 'sword' in inp:
            return self.look3
        else:
            return "Taken."



class Pos1_6_7(Place):
    enemy_spawn = False
    look1 = """
You find yourself at the south end of a long bridge that crosses the
river. Blocking your path is a large burly guard with a spear in one 
hand. His other hand is holding his sizeable navel. He keeps muttering
to himself "...must protect the bridge...must protect the bridge..." 
Maybe you could try to TALK to him?
"""
    look2 = """
You find yourself at the south end of a long bridge that crosses the
river. Over to the east sits the guard, contentedly munching on the 
goodwill pickle you gave him.
"""
    look3 = ["""
"Hey look here mister." You say. "I know it's against your code or
whatever to let someone pass without paying a toll so how about this:
I have here a pickle. You look famished and you need this pickle more
than I do. How about you let me pass in exchange for this pickle? How 
does that sound?"

The guard considers you carefully...

"Well..." He says slowly. "I suppose I could accept pickles as form of
payment." """,
"""
"Yeah!" You add quickly. "And if you take it I'll never tell the king 
and he'll never know." ...or he won't even care, you think to yourself
because you already know that the king was brutally murdered by the 
dragon so it's safe to say that he has bigger fish to fry at the 
moment...

The guard seems to be caving. "Yes...yes... he'll never know." He says
as he takes the pickle from you. """,
"""
The guard wistfully lumbers off to the east to the edge of the cliff 
and sits down. As he eats the pickle he continues to mutter under his
breath, "Yes...yummy pickle...yessss..."

You make a mental note that, should you ever become king, you will 
keep your guards well fed and happy. At any rate the bridge is now
clear for you to cross.
"""
]
    look4 = ["""
"Hello!" You say trying to sound cheerful. "Look, I don't mean to be a
bother but I would really like to get across this bridge. Is there any
a fine upstanding fellow like yourself could let me cross?"

He looks up and seems surprised that there is a person talking to him.

"I'm afraid not." He says in a ragged voice. "Not without paying the toll.
Everyone has to pay the toll!" """,
"""
"I don't have any money." You say. "But it would mean a lot if you would
let me pass. I am trying to save the kingdom you know." You say hopefully
but the large guard just shakes is head slowly.

"No one passes here without paying a toll! The king himself trusted old
Johnny here to keep this bridge. So I cannot let anyone pass without
paying a toll!" He says stubbornly. And you give up. There's no sense in
trying to reason with a man who's dogmatically stubborn and looks half
starved. You decide to leave him alone.  """
]
    look5 = """
"Yessss....good pickle...yummy pickle...yesss..." The guard doesn't appear to
want to talk. He has his pickle, you have a clear bridge and that is the 
end of it. 'Not a very social fellow', you think as you go your way.
"""
    def look(self):
        if self.guard_moved == True:
            here = self.look2
        else:
            here = self.look1
    
        return "%s\n%s %s" % (self.crdnts, here, self.item_here())
        
    def use(self, inp):
        if self.guard_moved == True:
            return "The guard already has a pickle."
        elif 'pickle' in inp:
            self.guard_moved = True
            self.blocked = False
            return self.look3, 'pickle'
        else:
            return "That item does you no good here."
    
    def talk(self, inp):
        if self.guard_moved == True:
            return self.look5
        else:
            return self.look4
    
    def go(self, inp):
        if 'north' in inp:
            return "\nYou can't go that way.\n"
        else:
            return None
    
    blocked = True
    i_consume = True
    guard_moved = False
    crdnts = [6, 7]
    items = []



class Pos1_man(Place):
    enemy_spawn = False
    look1 = [ """
Of course! The key! You dig around and pull it out. Maybe this key
wasn't so boring after all. You see that it fits in the lock on the
statue. You stick the key in the lock and turn and--

Suddenly you become aware of the ground rumbling beneath you. You try
to steady yourself on the statue then--

You are falling through the ground. You can feel the darkness overcome
you as the light of day dwindles and you fall down, down, down...		
""",
"""
...into what?
""", """
You land somewhere you don't know. It is dark and quiet. Silence...
You get to your feet ready for anything.
You take a step.""", """
And another...
""", """
Suddenly, a low red light flares up and you look around. You are in some
sort of tunnel that leads off to the WEST. It seems as if you have no
choice but to go WEST toward the light. """, """
As you draw nearer to the light you realize it is made by several 
torches that light the tunnel. You wonder who lit them...
You continue WEST.""", """
You are here.
""", """
You are somewhere in the mansion now. To the west is what used
to be the central atrium of the mansion. It is wrecked now. The
floor is cracked and there is stone and broken pillars that once
held up beautiful balconies littered about the hall. In the middle
of it all lies the dragon sleeping. The air is rank with a rotten
flesh smell. You slowly step forward for this is what you have come to
do. Run the dragon back to the distant land from whence it came.
Suddenly-- """, """
You accidentally trip over a rock that is near the top of the pile of
debris on which you are standing. The rock rolls down the pile making
a loud clatter as it rolls...oh no...""", """
The dragon awakes with a start. You didn't want this. You hoped you could
defeat the beast while he was sleeping. Now you must act, and act quickly.
But what do you do? Do you FIGHT him or FLEE? Or perhaps you could
HIDE among all the debris in the hall?"""
]
    
    look2 = """
The dragon is getting to his feet, looking around. He might spot you
at any moment. You must act, and act quickly. But what do you do? 
Do you FIGHT him or FLEE? Or perhaps you could HIDE among all the 
debris in the hall?
"""

    look3 = """
The dragon is looking in your general direction. He might spot you at
any moment. You must act, and act quickly. But what do you do? 
Do you FIGHT him or FLEE? Or perhaps you could HIDE among all the 
debris in the hall?
"""

    look4 = """The dragon's eyes fall on you. Your heart sinks as you realize that
you have been spotted. In a flash, the dragon blows a firey hurricane
in your direction. Unfortunatly at this point, there is no hope for you.
You burn to death in the dragon's fire. Maybe next time you should react
a little more quickly...
-- GAME OVER --
press Escape to exit...
"""
    look5 = """As you stand to fight the dragon's eyes fall on you. Your heart 
sinks as you realize that he really has the jump on you 
this time. In a flash, the dragon blows a firey hurricane in your 
direction. Unfortunatly at this point, there is no hope for you. You 
burn to death in the dragon's fire. Maybe next time you should look
before you leap...
-- GAME OVER --
press Escape to exit...
"""

    def look(self):
        self.incrementer += 1

        if self.incrementer == 2:
            return self.look2
        elif self.incrementer == 3:
            return self.look3
        elif self.incrementer > 3:
            return 'game over 1'
        else:
            return self.look1

    def fight(self, inp):
        return 'game over 2'
    
    def hide(self, inp):
        return 'change map--1.1'
        
    def flee(self, inp):
        return 'change pos--4,3'


    crdnts = [7, 1]
    items = []



class Pos1_7_4(Place):

    look1 = """
You are in a dimly lit corridor of trees that runs NORTH and SOUTH.
To the east and west of you lies nothing but dense forest.
"""
    crdnts = [7, 4]
    items = []



class Pos1_7_6(Place):

    look1 = """
You are in the middle of a large green meadow. Far to the west is
the dense forest. You see, looking north, a wide river, muddy from
spring run-off, flowing to the east. You see that further EAST there
is more meadow and a cliff. To the SOUTH is the cliff face of Red
Castle Mountain.
"""
    crdnts = [7, 6]
    items = []



class Pos1_7_7(Place):

    look1 = """
You are standing, facing east, near the edge of a cliff that
overlooks Nishai Valley. To the NORTH and WEST lies more
meadow. To the SOUTH lies a path that leads up the face of
the cliff toward Red Castle Mountain.
"""
    crdnts = [7, 7]
    items = []



class Pos1_8_4(Place):

    look1 = """
You find yourself at the entrance of a long corridor made of
trees. Originally, you did not notice this hole in the immensely
thick forest surrounding you.
From your point of view you can see that the dimly lit corridor
continues NORTH and the hole in the trees you just entered lies
to the EAST.
"""
    crdnts = [8, 4]
    items = []



class Pos1_8_5(Place):

    enemy_spawn = False
    look1 = """
You are standing in a clearing with dense woods surrounding you on the
WEST and north. To the EAST there is a large field which looks
inviting. To the south there is a cliff face which transitions
smoothly into the slopes of Red Castle Mountain. The part of the cliff
face that you can see from here looks unclimable.
"""
    crdnts = [8, 5]
    items = []



class Pos1_8_6(Place):

    look1 = """
As you walk along the cliff face looking up you can see mountain goats
making their way across the cliffs. You are now in a large field. The
sun shines brightly down on you and there isn't a cloud in the sky.
With Red Castle Mountain to your back you can see a large meadow that
stretches to the NORTH. To the EAST there is a path that leads up the
mountain. To the WEST you can see place where you started in the
clearing near the dense forest. Somewhere in the distance, you hear a
river or waterfall.
"""
    crdnts = [8, 6]
    items = []



class Pos1_8_7(Place):
    look1 = """
You climb up a mountain path until you happen upon a boulder that blocks
your way. There is a skull here stuck in the dirt which is soft directly
around it.
"""
    look2 = """
You dig through the dirt and unearth the fabled BIGKEY! YEAH!
Now we're getting somewhere!
"""	
    look3 = """
You already got the key. Move on.
"""
    look4 = """
You climb up a mountain path until you happen upon a boulder that blocks
your way. You left a sizable hole looking for that key. There's really
nothing left to see here except the hole you dug and the boulder.
"""
    def look(self):
        if self.hole_dug == True:
            here = self.look4
        elif self.hole_dug == False:
            here = self.look1
    
        return "%s\n%s %s" % (self.crdnts, here, self.item_here())

    def use(self, inp):
        if self.hole_dug == True:
            return self.look3
        elif 'shovel' in inp:
            self.hole_dug = True
            self.items.append('bigkey')
            return self.look2
        else:
            return "That item does you no good here."
            
    hole_dug = False
    crdnts = [8, 7]
    items = []

###############################################################################
#                                MANSION MAP                                  #
###############################################################################

class Pos1_man1_1(Place):

    look1 = """You are in the northwest corner of the hall. The balcony you see from here runs almost a complete circle around the hall.
The dragon is still alert listening for the slightest sound.

The balcony runs SOUTH and EAST from here.
"""

    crdnts = [1, 1]
    items = []



class Pos1_man1_2(Place):

    look1 = """You see the dragon whirl around at your footsteps and blow a fireball in your direction. The fireball collides with
north wall and extinguishes itself. You count yourself extremely lucky that you dodged quickly enough. You can hear the dragon's
low growl as looks around again.

The balcony runs EAST and WEST from here.
"""

    crdnts = [1, 2]
    items = []
    blocked  = True

    def go(self, inp):
        if 'south' in inp:
            return "\nYou can't go that way.\n"
        else:
            return None


class Pos1_man1_3(Place):

    look1 = """The dragon seems to be getting more paranoid. You must keep moving to avoid being seen.

The balcony runs EAST and WEST from here.
"""
    crdnts = [1, 3]
    items = []
    blocked  = True

    def go(self, inp):
        if 'south' in inp:
            return "\nYou can't go that way.\n"
        else:
            return None


class Pos1_man1_4(Place):

    look1 = """You have reached the northeast corner of the hall. To the SOUTH is an overlook that might make a good place to spy on
the dragon. The only other option at this point is to go back WEST. 
"""

    crdnts = [1, 4]
    items = []



class Pos1_man2_1(Place):

    look1 = """You are at the far south end of the hall. The dragon at this moment is looking to the north east and is
sniffing around a pile of debris. You feel lucky that he doesn't notice you. At the moment you feel a bit exposed.
It would be best to find a spot with more cover.

The balcony continues NORTH and SOUTH.
"""

    crdnts = [2, 1]
    items = []
    blocked  = True

    def go(self, inp):
        if 'east' in inp:
            return "\nYou can't go that way.\n"
        else:
            return None



class Pos1_man2_2(Place):
    enemy_spawn = False
    look1 = 'game over 2'

    crdnts = [2, 2]
    items = []
    
    def look(self):
        return self.look1



class Pos1_man2_3(Place):
    enemy_spawn = False
    look1 = 'game over 2'
    
    crdnts = [2, 3]
    items = []
    
    def look(self):
        return self.look1


class Pos1_man2_4(Place):
    enemy_spawn = False
    look1 = """You are now at the east end of the hall. The dragon still has not noticed you. As you survey the hall you see it. The ceiling is
cracked and almost ready to collapse on account of the dragon tearing down the pillars in this hall. You see that it is made of a Gothic 
structure that depends on keystone at the top of arch to stay erect. You realize that the chandelier is anchored to the ceiling on this 
keystone. A change in weight might make the entire hall collapse.

What do you do? You could CUT the rope that holds the chandelier.  You could CLIMB the rope and see if your weight brings down the hall.
Or you could THROW your sword at the chandelier to stab the dragon."""

    look_win_world1 = ["""
The Dragon shrieks in pain as you deliver your final blow. The Dragon begins to 
thrash around causing the stones and rubble that once made up the
ceiling come crashing down as you jump from the dragon and make for the
door. You reach it just in time as the dragon continues to thrash and
wail in pain. You run out the door just in time to see the mansion
collapse on itself. A deep red sunset makes a beautiful backdrop for
the triumphant scene. The mansion is destroyed but the dragon is
vanquished.""","""
You decide to rest as soon as you can. It has been, after all, a very
long day. But you know this is not the end but the beginning. More 
adventure awaits as you make your way out of the shadow of Red Castle
Mountain into the light of Nishai Valley where more trouble is brewing...
"""]

    crdnts = [2, 4]
    items = []
    blocked  = True

    def go(self, inp):
        if 'south' in inp:
            return "\nYou can't go that way.\n"
        elif 'west' in inp:
            return "\nYou can't go that way.\n"
        else:
            return None
    
    def cut(self, inp):
        return 'battle -50 hp dragon'
    
    def climb(self, inp):
        return 'battle dragon'
        
    def throw(self, inp):
        return 'game over 2'



class Pos1_man3_1(Place):

    look1 = """At the top of the stairs you pause a moment to catch your breath. This will not be easy. You find a good vantage
point to spy on the dragon as he continues to look suspiciously around the hall. You can't be sure but you think he can smell
you somewhere in here.

The top step lies in the southwest corner of the hall. The entrance to the hall is back to the EAST. The balcony extends
to the NORTH and is still mostly intact. 
"""

    crdnts = [3, 1]
    items = []



class Pos1_man3_2(Place):

    look1 = """It seems as though sneaking around isn't really your style so you try to pick up as much information as you can as you go.
You peek around your hiding place and notice that this dragon has a slight limp in his left hind leg. You remember this as you begin to
stratigize on how to bring this monster down.

You are at the foot of the staircase. It proceeds up and WEST. The entrance to the hall lies back EAST.    
"""

    crdnts = [3, 2]
    items = []



class Pos1_man3_3(Place):

    look1 = """
You are behind a pillar that blocks you from view of the dragon.
The dragon is definitely awake and alert now and is turning his 
head looking around the wrecked hall.
The dragon stands to the NORTH. To the EAST is where you came in
and to the WEST lies the staircase.
"""
    look2 = """You quickly jump behind a large boulder that lies around the edge of 
the hall. The dragon was startled but apparently didn't see you there because shouts, 
"Who's there!?" in his booming voice. You need to act quickly but what do you do? If you
stay put he might find you. At any rate you're not doing much good just sitting here.
The dragon is pacing back and forth to the NORTH. If you get too close you'll be spotted
and I don't think that will end well. To the EAST is where you came in and is an exposed
area. You will likely be seen. To the WEST is a staircase that leads to balcony that looks
down on the hall.
"""
    crdnts = [3, 3]
    items = []



class Pos1_man3_4(Place):

    look1 = 'game over 1'

    crdnts = [3, 4]
    items = []

    def look(self):
        return self.look1
    
class Map1():

    name = 'map1'
    pic_name = None

    spaces_dict = {
    'pos1_1_1': Pos1_1_1(),
    'pos1_1_2': Pos1_1_2(),
    'pos1_1_3': Pos1_1_3(),
    'pos1_1_4': Pos1_1_4(),
    'pos1_1_5': Pos1_1_5(),
    'pos1_2_5': Pos1_2_5(),
    'pos1_2_6': Pos1_2_6(),
    'pos1_3_5': Pos1_3_5(),
    'pos1_3_6': Pos1_3_6(),
    'pos1_3_7': Pos1_3_7(),
    'pos1_4_2': Pos1_4_2(),
    'pos1_4_3': Pos1_4_3(),
    'pos1_4_4': Pos1_4_4(),
    'pos1_4_5': Pos1_4_5(),
    'pos1_4_6': Pos1_4_6(),
    'pos1_4_7': Pos1_4_7(),
    'pos1_5_7': Pos1_5_7(),
    'pos1_6_4': Pos1_6_4(),
    'pos1_6_5': Pos1_6_5(),
    'pos1_6_7': Pos1_6_7(),
    'pos1_man': Pos1_man(),
    'pos1_7_4': Pos1_7_4(),
    'pos1_7_6': Pos1_7_6(),
    'pos1_7_7': Pos1_7_7(),
    'pos1_8_4': Pos1_8_4(),
    'pos1_8_5': Pos1_8_5(),
    'pos1_8_6': Pos1_8_6(),
    'pos1_8_7': Pos1_8_7(),
    }

    spaces = [
    [ None, None, None, None, None, None, None, None, None],
    [ None,'1_1','1_2','1_3','1_4','1_5', None, None, None],
    [ None, None, None, None, None,'2_5','2_6', None, None],
    [ None, None, None, None, None,'3_5','3_6','3_7', None],
    [ None, None,'4_2','4_3','4_4','4_5','4_6','4_7', None],
    [ None, None, None, None, None, None, None,'5_7', None],
    [ None, None, None, None,'6_4','6_5', None,'6_7', None],
    [ None,'man', None, None,'7_4', None,'7_6','7_7', None],
    [ None, None, None, None,'8_4','8_5','8_6','8_7', None],
    [ None, None, None, None, None, None, None, None, None]
    ]
# note that 'man' is in [7][1]

    def pos(self,row,column):
        """ returns the value of the space to be translated into the 
        dictionary"""
        pos1 = self.spaces[row][column]
        if pos1 == None:
            return "\nYou can't go that way.\n"
        pos1_name =  "pos1_%s" % pos1
        return self.spaces_dict[pos1_name]
        
class Map1_1(Map1):

    pic_name = 'mans'

    spaces_dict = {
        'pos1_man1_1': Pos1_man1_1(),
        'pos1_man1_2': Pos1_man1_2(),
        'pos1_man1_3': Pos1_man1_3(),
        'pos1_man1_4': Pos1_man1_4(),
        'pos1_man2_1': Pos1_man2_1(),
        'pos1_man2_2': Pos1_man2_2(),
        'pos1_man2_3': Pos1_man2_3(),
        'pos1_man2_4': Pos1_man2_4(),
        'pos1_man3_1': Pos1_man3_1(),
        'pos1_man3_2': Pos1_man3_2(),
        'pos1_man3_3': Pos1_man3_3(),
        'pos1_man3_4': Pos1_man3_4(),
    }

    spaces = [
    [ None, None,   None,    None,    None,    None],
    [ None,'man1_1','man1_2','man1_3','man1_4',None],
    [ None,'man2_1','man2_2','man2_3','man2_4',None],
    [ None,'man3_1','man3_2','man3_3','man3_4',None],
    [ None, None,   None,    None,    None,    None],
    ]

#########################  END OF WORLD 1 MAP SECTION  ########################        

###############################################################################
#                           GAME GUI FROM TKINTER                             #
###############################################################################

class GameGUI(Frame):
  
    def __init__(self, parent, engine):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.engine = engine
        self.intro = """
Welcome to RCA World 1! A world of exploring adventure and defeating
evil awaits! You are the intrepid explorer/adventurer/evil defeater 
known throughout the land as "Larry". However, you are about to
embark on your greatest quest yet in the shadow of Red Castle Mountain.
Good luck adventurer!

Press ENTER to begin!
"""
        self.initUI()
        
    def initUI(self):
        
        self.parent.configure(background='black')
        self.configure(background='black')
        self.parent.title("Red Castle Avenger")
        self.parent.bind("<Escape>", lambda self: self.widget.quit())
        
        img = Image.open("intro2.jpg")
        w, h = img.size
        new_w, new_h = self.pic_size(w, h)
        resized = img.resize((new_w, new_h), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(resized)
        self.panel = Label(self.parent, image=pic) 
        self.panel.image = pic
        self.panel.configure(bg='black')
        
        self.canvas = Canvas(self)
        self.canvas.configure(background='black')
        self.text = self.canvas.create_text(20, 30, anchor=NW,
            font="Papyrus", fill='white', text=self.intro)

        self.v = StringVar(self.parent)
        e = Entry(self.parent, textvariable=self.v)
        l = Label(self.parent, text='> ')
        l.configure(bg='black', fg ='white', font='Papyrus')
        e.config(bg='black', fg ='white', font='Papyrus')
        self.v.set('')

        self.panel.pack(fill=BOTH)
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)
        l.pack(side=LEFT)
        e.pack(fill=BOTH)

        self.parent.bind("<Return>", self.do_it)
        e.focus_set()
        
        self.start = 0
        self.pos_pic = None
        self.big_text = False
        self.increments = 0
        self.big_out = None
    
    def do_it(self, event):
        if self.big_text == True:
            return self.a_lotta_text()
        else:
            return self.play_the_game()

    def play_the_game(self):
        text = self.v.get()
        self.v.set('')
        print text
        if self.start == 0:
            text = 'look'
            self.start = 1

        out1, pos = self.engine.process_inp(text)
        
        if pos == 'game state':
            out1 = self.game_state(out1)
            pos = self.engine.player.position.crdnts
            
        if out1 == 'MAP':
            map_name = self.engine.player.map.name
            new_pos_pic = 'RCAmap_%s.jpg' % map_name
        elif out1 == "-- GAME OVER --\n   press Escape to exit...":
            new_pos_pic = 'pos1_gm_ovr.jpg'
        elif pos == 'win1':
            new_pos_pic = 'pos1_win.jpg'
        elif pos == 'battle':
            new_pos_pic = 'pos1_battle_%s.jpg' % self.engine.player.enemy.name
        elif self.engine.player.map.pic_name == 'mans':
            new_pos_pic = 'pos1_man%s_%s.jpg' % (pos[0], pos[1])
        else:
            new_pos_pic = 'pos1_%s_%s.jpg' % (pos[0], pos[1])

        try:
            if new_pos_pic != self.pos_pic:
                self.pos_pic = new_pos_pic
                img1 = Image.open(self.pos_pic)
                w, h = img1.size
                new_w, new_h = self.pic_size(w, h)
                img1 = img1.resize((new_w, new_h), Image.ANTIALIAS)
                img1 = ImageTk.PhotoImage(img1)
                self.panel.configure(image=img1)
                self.panel.image = img1
        except:
            print "Picture Error!"
            
        if not isinstance(out1, basestring):
            self.big_text = True
            self.big_out = out1
            self.do_it(None)
            return None

        self.canvas.dchars(self.text,0,END)
        self.canvas.insert(self.text,0,out1)

            
    def a_lotta_text(self):
        if self.increments < len(self.big_out)-1:
            out = "%s...\nPress ENTER to continue..."\
                % self.big_out[self.increments]
            self.canvas.dchars(self.text,0,END)
            self.canvas.insert(self.text,0,out)
            self.increments += 1
        elif self.increments < len(self.big_out):
            out = "%s" % self.big_out[self.increments]
            self.canvas.dchars(self.text,0,END)
            self.canvas.insert(self.text,0,out)
            self.increments += 1
        else:
            self.increments = 0
            self.big_text = False
            self.big_out = None
            self.do_it(None)
            
    def pic_size(self, w, h):

        a_r = float(w)/float(h)
        h_max = .5 * self.parent.winfo_screenheight()
        w_new = int(h_max * a_r)
        h_max = int(h_max)
        return w_new, h_max
        
    def game_state(self, inp):
        name = 'game'
        if inp[0] == 'save':
            with open(name, "wb") as f:
                dump(self.engine, f)
            return "%s saved" % name
        elif inp[0] == 'load':
            with open(name, "rb") as f:
                self.engine = load(f)
            return "%s loaded" % name
        else:
            return "I don't understand that."

def play_gui():
    app = initialize()
    
    root1 = Tk()
    ex = GameGUI(root1, app)
    w, h = root1.winfo_screenwidth(), root1.winfo_screenheight()
    root1.overrideredirect(1)
    root1.geometry("%dx%d+0+0" % (w, h))
    root1.mainloop()  
    
def initialize():
    pos1 = Pos1_8_5()
    world1 = Map1()
    user1 = Player1(pos1, world1)
    in_take = Parser()
    app = Engine(in_take, user1)
    return app

def main():
        play_gui()

if __name__ == '__main__':
    main()