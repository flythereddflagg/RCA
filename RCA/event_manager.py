# event_manager.py
from constants import *
from itertools import compress


class EventManager():
    """
    The purpose of thsi class is to capture any events from the user.
    In-game events will be captured by the game logic (i.e. the logic manager).
    """
    def __init__(self, eng):
        self.eng    = eng
        self.logic  = self.eng.logic
        

    def events(self):
        """
        Captures all events input by the user.
        """
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.eng.running = False
        
        keys = pg.key.get_pressed()
        #print(keys)
        key_ind = list(compress(range(len(keys)), keys))
        print(key_ind)
        if len(key_ind) > 1:
            print("input sensed")
            for i in key_ind:
                self.logic.key_do(i)
        else:
            print("no input registered")
            self.logic.no_key()

