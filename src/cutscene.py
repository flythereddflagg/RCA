from .decal import Decal
from .animation import Animation

class Move():
    direction = "UP"

class CutScene(Decal):
    def __init__(self, **options):
        super().__init__(**options)
        self.state = "intro"
        self.move = Move()
        self.animation = Animation(
            self, self.options['animations'], self.options["path_prefix"]
        )
        self.animation.previous = "titlescreen"

        
        
    
    def update(self):
        self.animation.update()
        self.rect.topleft = [0, 0]
        