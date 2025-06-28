from .decal import Decal
from .animation import Animation

class Move():
    direction = "UP"

class CutScene(Decal):
    def __init__(self, **init):
        super().__init__(**init)
        self.state = "intro"
        self.move = Move()
        self.animation = Animation(
            self, self.init['animations'], self.init["path_prefix"]
        )
        self.animation.previous = "titlescreen"

        
        
    
    def update(self):
        self.animation.update()
        self.rect.topleft = [0, 0]
        