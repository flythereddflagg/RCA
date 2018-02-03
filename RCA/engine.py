"""
File          : engine.py
Author        : Mark Redd
Last Modified : 180120

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

import pygame as pg
from player import Player
from background import Bg1


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
        self.FPS = 30
        self.running = True
        self.clock = pg.time.Clock()
        self.SCREENWIDTH = 800
        self.SCREENHEIGHT = 600
         
        self.size = (self.SCREENWIDTH, self.SCREENHEIGHT)
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption("A rectangle.")
        self.all_sprites_list = pg.sprite.Group()
        self.bgs = pg.sprite.Group()
        self.plr = Player()
        self.all_sprites_list.add(self.plr)
        for i in range(8):
            for j in range(6):
                x = Bg1(i*100,j*100)
                self.bgs.add(x)
    
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
            self.events()
            self.logic()
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)
        pg.quit()
    
    def events(self):
        """
        Handles all events in the game and produces appropriate commands
        to be fed to the logic function.
        """
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.plr.moveLeft(5)
        elif keys[pg.K_RIGHT]:
            self.plr.moveRight(5)
        elif keys[pg.K_UP]:
            self.plr.moveUp(5)
        elif keys[pg.K_DOWN]:
            self.plr.moveDown(5)
        else:
            self.plr.stand()

    def logic(self):
        """
        Executes necessary game logic and decides what the next frame should 
        look like
        """
        self.all_sprites_list.update()
        self.bgs.update()

    def draw(self):
        """
        Using the information from the logic method, draws the next frame.
        """
        self.screen.fill((119,119,119))
        #self.draw_background()
        self.bgs.draw(self.screen)
        self.all_sprites_list.draw(self.screen)
        pg.display.flip()
    
        
        
    

def main():
    eng = Engine()
    eng.mainloop()

if __name__ == '__main__':
    main()