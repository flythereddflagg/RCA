# logic_manager.py
from constants import *


class LogicManager():
    
    def __init__(self, eng):
        self.eng = eng
        self.all_sprites = self.eng.all_sprites
        self.background = self.eng.background
        
    
    def logic(self):
        self.all_sprites.update()
        self.background.update()
