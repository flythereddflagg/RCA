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
#from player import Player
#from background import Background
from event_manager import EventManager
from logic_manager import LogicManager
from drawing_manager import DrawingManager
#from zone1 import Zone1



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
        self.screen = pg.display.set_mode(SCREENSIZE)
        pg.display.set_caption("RCA")
        
        # Set up all sprite groups
        self.all_sprites = pg.sprite.Group() # everything
        self.background  = pg.sprite.Group() # background tiles
        self.players     = pg.sprite.Group() # sprites you can control
        self.blocks      = pg.sprite.Group() # non-moving sprites
        self.friends     = pg.sprite.Group() # moving friendly sprites
        self.foes        = pg.sprite.Group() # enemies
        self.hud         = pg.sprite.Group() # HUD (health, money etc.)
        self.misc        = pg.sprite.Group() # other (dialog boxes etc.)
        
        # Set up the various managers
        self.draw  = DrawingManager(self)
        self.logic = LogicManager(self)
        self.event = EventManager(self)
    
    def mainloop(self):
        """
        Running this function will execute the initialized game. The loop will
        continue as follows:
            while running
                get events (key strokes)
                figure out what should happen in the next frame
                    (incorperate in-game events)
                draw the next frame
            end the game when the loop exits
        """
        
        while self.running:
            self.event.events()
            self.logic.logic()
            self.draw.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        pg.quit()
  

def main():
    eng = Engine()
    eng.mainloop()

if __name__ == '__main__':
    main()

