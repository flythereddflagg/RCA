from .decal import Decal
from .tools import list_collided

EMPTY = 'empty'

class Item(Decal):
    def __init__(self, **init):
        super().__init__(**init)
        self.action = init.get("action")
    
    def update(self):
        self.check_collision()

    def check_collision(self):
        if self.id == EMPTY: return
        for player in list_collided(self, self.scene.groups['player']):
            print("\n\n###trying to add item to player! 1\n\n")
            if player.parent: player = player.parent
            if player.inventory:
                print("\n\n###trying to add item to player!\n\n")
                new_slot = player.inventory.add_item(self)
                if new_slot is None: return # no more slots can be added
                self.kill()
            break
