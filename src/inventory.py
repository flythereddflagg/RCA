from .item import Item
from .decal import Decal
from .tools import get_center_screen

N_SLOTS = 8

class Inventory(Decal):
    def __init__(
        self, scene, money:int=0, hp:int=0, hp_max:int=0, max_money=999
    ):
        super().__init__(**{
                "id": "inventory_screen",
                "scene": scene,
                "image": "./assets/actor/inventory_screen/backpack.png",
                "mask": None,
                "scale": 2
        })
        self.slots = [None for _ in range(N_SLOTS)]
        self.money:int = money # gold coins
        self.hp:int = hp
        self.HP_MAX:int = hp_max
        self.max_money = max_money
        self.active = False

        self.rect.center = get_center_screen()
        self.scene.layers['hud'].add(self)
        

    def update(self):
        if self.scene.player.keys_held["BUTTON_3"] and not self.alive():
            self.active = True
            self.scene.layers['hud'].add(self)
        
        if not self.scene.player.keys_held["BUTTON_3"] and self.alive():
            self.active = False
            self.kill()


    def change_money(self, amount:int):
        new_amount = self.money + amount
        if new_amount < 0:
            return -1 # this cannot happen

        if new_amount > self.max_money:
            new_amount = self.max_money
        
        self.money = new_amount


    def change_health(self, amount:int) -> int:
        self.hp = self.hp + amount if self.hp + amount > 0 else 0
        self.hp = self.hp if self.hp < self.HP_MAX else self.HP_MAX
        return self.hp


    def add_slot(self):
        for i, slot in enumerate(self.slots):
            if slot is None:
                self.slots[i] = Item('empty')
                return self.slots[i]
        
        return None


    def add_item(self, item:Item):
        for i, slot in enumerate(self.slots):
            if slot.id is 'empty':
                self.slots[i] = item
                return self.slots[i]
        
        return None


    def remove_item(self, id_:str):
        for i, slot in enumerate(self.slots):
            if slot.id == id_:
                self.slots[i] = Item('empty')
                return self.slots[i]
        
        return None
