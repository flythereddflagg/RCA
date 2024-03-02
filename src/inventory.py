import pygame as pg

from .item import Item
from .decal import Decal
from .tools import get_center_screen
from .compass import Compass

N_SLOTS = 6

class Inventory(Decal):
    def __init__(
        self, player, money:int=0, hp:int=0, hp_max:int=0, max_money=999
    ):
        super().__init__(**{
                "id": "inventory_screen",
                "scene": player.scene,
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
        self.player = player
        self.rect.center = get_center_screen()

        self.slot_sprites = pg.sprite.Group()
        angle = rot_gen()
        for i in range(N_SLOTS):
            new_slot = Decal(**{
                "id": f"inventory_slot({i})",
                "scene": player.scene,
                "image": "./assets/actor/inventory_screen/slot.png",
                "mask": None,
                "scale": 1
            })
            new_slot.rect.center = (
                pg.math.Vector2(self.rect.center) + 
                (pg.math.Vector2(Compass.unit_vector(Compass.UP)) * 
                    self.image.get_height()
                # ).rotate(i / N_SLOTS * 360)
                ).rotate(2 * 360 / N_SLOTS * i + 360 / N_SLOTS * (i//(N_SLOTS//2)))
            )
            self.slot_sprites.add(new_slot)


    def update(self):
        # update reference to scene if necessary
        if self.player.scene is not self.scene: 
            self.scene = self.player.scene
        if self.player.keys_held["BUTTON_3"] and not self.active:
            self.active = True
            self.toggle()
        
        if not self.player.keys_held["BUTTON_3"] and self.active:
            self.active = False
            self.toggle()
        
        
    def toggle(self):
        toggle_state = (
            self.scene.layers['hud'].add 
            if self.active else 
            self.scene.layers['hud'].remove
        )
        toggle_state(self)
        for i, slot in enumerate(self.slots):
            if slot is None: continue
            toggle_state(self.slot_sprites.sprites()[i])
            

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
            if slot.id == 'empty':
                self.slots[i] = item
                return self.slots[i]
        
        return None


    def remove_item(self, id_:str):
        for i, slot in enumerate(self.slots):
            if slot.id == id_:
                self.slots[i] = Item('empty')
                return self.slots[i]
        
        return None
