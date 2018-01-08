"""
main program flow
Start
Define and open a new window
Set up all your sprites and backgrounds

while running
    get events (key strokes and stuff)
    figure out what should happen in the next frame
    draw the next frame
end

based on: http://www.101computing.net/pygame-how-tos/
"""

import pygame as pg


class Engine():
    def __init__(self, FPS):
        pg.init()
        self.FPS = FPS
        self.running = True
        self.clock = pg.time.Clock()
        self.SCREENWIDTH = 800
        self.SCREENHEIGHT = 600
         
        self.size = (self.SCREENWIDTH, self.SCREENHEIGHT)
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption("A caption for your game")
    
    def mainloop(self):
        while self.running:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.running = False
            self.events()
            self.logic()
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)
        pg.quit()
    
    def events(self):
        pass

    def logic(self):
        pass

    def draw(self):
        pass


def main():
    eng = Engine(30)
    eng.mainloop()

if __name__ == '__main__':
    main()