from .decal import Decal
from .tools import list_collided

EMPTY = 'empty'

class Item(Decal):
    def __init__(self, **options):
        self.id = options['id']
        if self.id == EMPTY:
            self.sprite = None
            return
        super().__init__(**options)
        self.action = options["action"]
    
    def __repr__(self):
        return f"<Item - {self.id}>"

    def select(self):
        return self.action
    
    def update(self):
        self.check_collision()

    def check_collision(self):
        if self.id == EMPTY: return
        for player in list_collided(self, self.scene.groups['player']):
            if player.inventory:
                new_slot = player.inventory.add_item(self)
                if new_slot is None: return # no more slots can be added
                self.kill()
            break