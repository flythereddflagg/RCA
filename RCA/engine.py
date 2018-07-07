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
from itertools import compress
from rca_game import RCAGame

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
        self.accept_input = True
        
        # Set up the game manager
        self.game = RCAGame(self)
    
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
            self.events()
            self.game.logic() # game logic here
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        pg.quit()
    
    
    def events(self):
        """
        Captures all events input by the user. Then calls on the game
        object to execute any neccesary commands
        """

        for event in pg.event.get():
            #print(event)
            self.game.event_do(event)
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_BACKSPACE]:
            self.running = False
        
            
        key_indices = list(compress(range(len(keys)), keys))
        # disregard numlock key
        if pg.K_NUMLOCK in key_indices: key_indices.remove(pg.K_NUMLOCK)
        print(key_indices)
        if not self.accept_input: return
        if key_indices:
            for i in key_indices:
                self.game.key_do(i) 
        else:
            self.game.no_key()

    
    def draw(self):
        """
        Once the game logic method has run, this function updates all sprites
        based on what the logic method did and then draws the next frame in an
        order specified by the game manager.
        """
        self.game.all_sprites.update()
        self.screen.fill(BLACK)
        for group in self.game.groups_list:
            group.draw(self.screen)


def main():
    eng = Engine()
    eng.mainloop()

if __name__ == '__main__':
    main()

