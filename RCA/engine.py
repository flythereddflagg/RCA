"""
File          : engine.py
Author        : Mark Redd

main program flow
Start
Define and open a new window
Set up all your sprites and backgrounds

while running
    get events (key strokes and stuff)
    figure out what should happen in the next frame
    draw the next frame
end

based on: http://www.101computing.net/pg-how-tos/
"""
from constants import *
from player import Player
from background import BackgroundTest
from event_manager import EventManager
from logic_manager import LogicManager
from drawing_manager import DrawingManager



class Engine():
    def __init__(self, config = None):
        """
        Receives a dictionary (config) with all the keys being configuration 
        variables and the coplresponding values. Uses these to configure and 
        initialize the game. Must do the following:
            - Start
            - Set up the configuration
            - Define and open a new window
            - Set up all your sprites and backgrounds
        """
        pg.init()
        self.running = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(SCRNSIZE)
        pg.display.set_caption("RCA")
        self.all_sprites = pg.sprite.Group() # everything
        self.background  = pg.sprite.Group() # background tiles
        self.players     = pg.sprite.Group() # sprites you can control
        self.blocks      = pg.sprite.Group() # non-moving sprites
        self.friends     = pg.sprite.Group() # moving friendly sprites
        self.foes        = pg.sprite.Group() # enemies
        self.hud         = pg.sprite.Group() # HUD (health, money etc.)
        self.misc        = pg.sprite.Group() # other (dialog boxes etc.)
        # set up player
        self.player = Player(self)
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        for i in range(8):
            for j in range(8):
                x = BackgroundTest(i*100,j*100)
                self.background.add(x)
                self.all_sprites.add(x)
        
        self.eman = EventManager(self)
        self.lman = LogicManager(self)
        self.dman = DrawingManager(self)
    
    def mainloop(self):
        """
        Running this function will execute the initialized game. The loop will
        continue as follows:
            while running
                get events (key strokes and stuff)
                figure out what should happen in the next frame
                draw the next frame
            end the game when the loop exits
        """
        
        while self.running:
            self.eman.events()
            self.lman.logic()
            self.dman.draw()
            pg.display.flip()
            self.clock.tick(FPS)
  
  

def main():
    eng = Engine()
    eng.mainloop()

if __name__ == '__main__':
    main()
