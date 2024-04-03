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
            "scale": 1
        })

        self.slots:list[Item] = []
        self.money:int = money # gold coins
        self.hp:int = hp
        self.HP_MAX:int = hp_max
        self.max_money = max_money
        self.active = False
        self.player = player
        self.left_item:Item = self.empty_item()
        self.right_item:Item = self.empty_item()
        self.rect.center = get_center_screen()

        self.slot_sprites = pg.sprite.Group()

        self.left_hand, self.right_hand = (Decal(**{
                "id": "inventory_screen",
                "scene": player.scene,
                "image": "./assets/actor/inventory_screen/hand.png",
                "mask": None,
                "scale": 1
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
        self.marker = Decal(**{
            "id": "inventory_marker",
            "scene": player.scene,
            "image": "./assets/actor/inventory_screen/marker.png",
            "mask": None,
            "scale": 1
        })
        self.marker.rect.center = self.rect.center
        # TODO make marker select an inventory slot


    def update(self):
        # update reference to scene if necessary
        if self.player.scene is not self.scene: 
            self.scene = self.player.scene

        input_held = self.player.scene.game.input.held
        
        if not any([input_held[key] for key in ["R_UP","R_DOWN","R_LEFT","R_RIGHT"]]):
            if self.active: self.toggle()
            self.marker.rect.center = self.rect.center

        
    def toggle(self):
        self.active = False if self.active else True
        toggle_state = (
            self.scene.layers['hud'].add 
            if self.active else 
            self.scene.layers['hud'].remove
        )
        # ORDER MATTERS first we do the backpack and hands
        for sprite in [self, self.left_hand, self.right_hand]:
            toggle_state(sprite)

        # then we do the slots
        n_slots = len([slot for slot in self.slots if slot])
        for i, slot_sprite in enumerate(self.slot_sprites.sprites()):
            toggle_state(slot_sprite)
            slot_sprite.rect.center = (
                pg.math.Vector2(self.rect.center) + 
                (pg.math.Vector2(Compass.unit_vector(Compass.UP)) * 
                    self.image.get_height()
                ).rotate(i / n_slots * 360)
            )
        # then the sprites over the slots
        for slot_sprite, item in zip(self.slot_sprites.sprites(), self.slots):
            toggle_state(item)
            item.rect.center = slot_sprite.rect.center

        # finally the hand items and the marker goes LAST
        for sprite in [self.left_item, self.right_item, self.marker]:
            toggle_state(sprite)


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
        if len(self.slots) > N_SLOTS: return None
        self.slots.append(None)
        self.slots[-1] = self.empty_item()
        new_slot = Decal(**{
            "id": f"inventory_slot({len(self.slots)-1})",
            "scene": self.player.scene,
            "image": "./assets/actor/inventory_screen/slot.png",
            "mask": None,
            "scale": 1
        })
        self.slot_sprites.add(new_slot)
        return self.slots[-1]


    def add_item(self, item:Item):
        if self.left_item.id == 'empty':
            self.left_item = item
            self.left_item.rect.center = self.left_hand.rect.center
            return item
        if self.right_item.id == 'empty':
            self.right_item = item
            self.right_item.rect.center = self.right_hand.rect.center
            return item
        for i, slot in enumerate(self.slots):
            if  slot.id == 'empty':
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
                self.slots[i] = self.empty_item()
                return self.slots[i]
        
        return None

    def get_selected_item_slot(self):
        indices = self.marker.rect.collidelistall(
            self.slot_sprites.sprites()
        )
        if not indices: return None
        return indices[0]


    def empty_item(self):
        return Item(**{
            'id' : 'empty',
            "image" : "./assets/block/null.png",
            "scene" : self.player.scene,
            'mask' : None,
            'action': None
        })


    def select(self, hand:str) -> Item:
        i_select = self.get_selected_item_slot()
        if i_select is None: return None
        selected_item:Item = self.slots[i_select]
        if selected_item is None: return None
        if hand.lower()[0] == 'r':
            self.slots[i_select] = self.right_item
            self.right_item = selected_item
            self.right_item.rect.center = self.right_hand.rect.center
            self.slots[i_select].rect.center = (
                self.slot_sprites.sprites()[i_select].rect.center
            )
            return self.right_item
        if hand.lower()[0] == 'l':
            self.slots[i_select] = self.left_item
            self.left_item = selected_item
            self.left_item.rect.center = self.left_hand.rect.center
            self.slots[i_select].rect.center = (
                self.slot_sprites.sprites()[i_select].rect.center
            )
            return self.left_item
        return None
        

