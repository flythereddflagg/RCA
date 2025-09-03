from .decal import Decal
from .animation import Animation

class Move():
    direction = "UP"

class CutScene(Decal):

    def setup(self):
        super().setup()
        self.state = "titlescreen"
        # self.state = "intro"
        self.move = Move()

    
    def update(self):
        self.animation.update()
        self.rect.topleft = [0, 0]
        