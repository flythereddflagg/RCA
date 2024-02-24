from .item import Item

N_SLOTS = 8

class Inventory():
    def __init__(self, money:int=0, hp:int=0, hp_max:int=0):
        self.slots = [None for _ in range(N_SLOTS)]
        self.money:int = money # gold coins
        self.hp:int = hp
        self.HP_MAX:int = hp_max
        

    def change_money(self, amount:int):
        new_amount = self.money + amount
        if new_amount < 0:
            return -1 # this cannot happen
        
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
