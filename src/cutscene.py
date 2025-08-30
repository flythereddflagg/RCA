from .decal import Decal
from .animation import Animation

class Move():
    direction = "UP"

class CutScene(Decal):

    def setup(self):
        super().setup()
        self.state = "intro"
        self.move = Move()
        # self.animation = Animation(
        #     self, self.init['animation'], self.init["path_prefix"]
        # )
        # self.animation.previous = "titlescreen"

    
    def update(self):
        self.animation.update()
        self.rect.topleft = [0, 0]
        