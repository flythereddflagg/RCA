# drawing_manager.py
from constants import *

class DrawingManager():
    def __init__(self, eng):
        self.eng        = eng
        self.screen     = self.eng.screen
        self.background = self.eng.background
        self.players    = self.eng.players   
        self.blocks     = self.eng.blocks    
        self.friends    = self.eng.friends   
        self.foes       = self.eng.foes      
        self.hud        = self.eng.hud       
        self.misc       = self.eng.misc

    def draw(self):
        """
        Using the information from the logic method, draws the next frame.
        """
        self.screen.fill(BLACK)
        self.background.draw(self.screen)
        self.blocks.draw(self.screen)
        self.players.draw(self.screen)
        self.friends.draw(self.screen)
        self.foes.draw(self.screen)
        self.hud.draw(self.screen)
        self.misc.draw(self.screen)

