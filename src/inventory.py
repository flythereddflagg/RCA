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
        self.left_item:Item = None
        self.right_item:Item = None
        self.slots:list[Item] = [None for _ in range(N_SLOTS)]
        self.money:int = money # gold coins
        self.hp:int = hp
        self.HP_MAX:int = hp_max
        self.max_money = max_money
        self.active = False
        self.player = player
        self.rect.center = get_center_screen()

        self.slot_sprites = pg.sprite.Group()
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
                ).rotate(
                    2 * 360 / N_SLOTS * i + 360 / N_SLOTS * (i//(N_SLOTS//2))
                )
            )
            self.slot_sprites.add(new_slot)
        
        self.left_hand, self.right_hand = (Decal(**{
                "id": "inventory_screen",
                "scene": player.scene,
                "image": "./assets/actor/inventory_screen/hand.png",
                "mask": None,
                "scale": 2
            })
            for _ in range(2)
        )
        self.right_hand.image = pg.transform.flip(
            self.right_hand.image, True, False
        ) # get the right hand where you want it

        self.left_hand.rect.center = self.rect.center + pg.math.Vector2(
            -self.rect.center[0]//2, 0
        )
        self.right_hand.rect.center = self.rect.center + pg.math.Vector2(
            self.rect.center[0]//2, 0
        )


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
        inventory_sprites = [
            self, self.left_hand, self.right_hand, 
            self.left_item, self.right_item
        ]
        for sprite in inventory_sprites:
            if sprite is None: continue
            toggle_state(sprite)

        for i, slot in enumerate(self.slots):
            if slot is None: continue
            toggle_state(self.slot_sprites.sprites()[i])
            if slot.id == 'empty': continue
            toggle_state(slot)
            

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
                self.slots[i] = Item(id='empty')
                return self.slots[i]
        
        return None


    def add_item(self, item:Item):
        if self.left_item is None:
            self.left_item = item
            self.left_item.rect.center = self.left_hand.rect.center
            return item
        if self.right_item is None:
            self.right_item = item
            self.right_item.rect.center = self.right_hand.rect.center
            return item
        for i, slot in enumerate(self.slots):
            if slot is not None and slot.id == 'empty':
                print(f"adding item {item}")
                self.slots[i] = item
                self.slots[i].rect.center = (
                    self.slot_sprites.sprites()[i].rect.center
                )
                return self.slots[i]
        
        return None


    def remove_item(self, id_:str):
        for i, slot in enumerate(self.slots):
            if slot.id == id_:
                self.slots[i] = Item('empty')
                return self.slots[i]
        
        return None


    def select(self, item:Item):
        pass

