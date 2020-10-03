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
    def __init__(self, game):
        """
        Must do the following:
            - Start pygame
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
        self.key_indices = []
        
        # Set up the game manager
        self.game = game(self)
    
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
        object to execute any necessary commands
        """
        for event in pg.event.get():
            self.game.event_do(event)
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_BACKSPACE]:
            self.running = False
            return
        
        
        if not self.accept_input: return
        
        old_keys = self.key_indices
        self.key_indices = list(compress(range(len(keys)), keys))

        # disregard numlock key
        if pg.K_NUMLOCK in self.key_indices: key_indices.remove(pg.K_NUMLOCK)
        
        off_keys = list(set(old_keys).difference(self.key_indices))
                
        for key in off_keys:
            self.game.off_key_do(key)
        
        if self.key_indices:
            for i in self.key_indices:
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
    eng = Engine(RCAGame)
    eng.mainloop()

if __name__ == '__main__':
    main()

