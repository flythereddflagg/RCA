import types

import pygame as pg

from .item import Item
from .decal import Decal
from .tools import list_collided, vec
from .compass import Compass
from .node import Node

N_SLOTS = 6
INV_SCALE = 1
LEFT_HAND_BUTTON = "BUTTON_S"
RIGHT_HAND_BUTTON = "BUTTON_E"
RIGHT_STICK_AX = ["R_"+direction for direction in Compass.strings]
LEFT_STICK_AX = [direction for direction in Compass.strings]
EMPTY = "empty"
HP_PER_DECAL = 3

class Inventory(Node):

    def setup(self):
        self.inventory_sprite = Decal(**{
            "parent": self,
            "id": "inventory_screen",
            "image": "./assets/actor/inventory_screen/backpack.png",
        })
        self.marker = Decal(**{
            "parent": self,
            "id": "inventory_marker",
            "image": "./assets/actor/inventory_screen/marker_icon.png",
        })
        self.left_hand, self.right_hand = (
            Decal(**{
                "id": f"inventory_hand_{i}",
                "image": "./assets/actor/inventory_screen/hand.png",
            })
            for i in range(2)
        )
        self.left_glyph = Decal(**{
            "id": f"inventory_glyph_A",
            "image": "./assets/block/glyph_A.png",
        })
        self.right_glyph = Decal(**{
            "id": f"inventory_glyph_B",
            "image": "./assets/block/glyph_B.png",
        })
        self.money_decal = Decal(id="money_decal")
        self.coin_decal = Decal(id="coin", image="./assets/block/coin.png")
        self.money_text = pg.font.Font("./assets/fonts/BoldPixels.ttf", 16)

        self.slots:list[Item] = []
        self.money:int = self.init.get("money", 0) # gold coins
        self.max_money = self.init.get("max_money", 999)
        self.hp:int = self.init.get("hp", 0)
        self.hp_max:int = self.init.get("hp_max", 10)
        self.active = False

        self.life_meter_decal = Decal(**{
            "id": f"heart_decal",
            "image": "./assets/block/heart.png",
        })
        nhearts = self.hp_max // HP_PER_DECAL
        new_surf = pg.Surface(
            (vec(self.life_meter_decal.rect.size).elementwise()
            * vec((nhearts, 1))),
            flags=pg.SRCALPHA
            
        )
        for i in range(nhearts):
            new_surf.blit(
                self.life_meter_decal.image, 
                (self.life_meter_decal.rect.size[0] * i, 0)
            )

        self.life_meter_decal.set_image(new_surf)

        self.life_meter = Decal(id="life_meter")
        self.life_meter.set_image(pg.Surface(
            self.life_meter_decal.rect.size, flags=pg.SRCALPHA
        ))
        self.life_meter.rect.topleft = (10, 10)

        self.left_item:Item = self.empty_item()
        self.right_item:Item = self.empty_item()
        self.inventory_sprite.rect.center = self.scene.game.get_center()

        self.slot_sprites = pg.sprite.Group()
        
        self.right_hand.image = pg.transform.flip(
            self.right_hand.image, True, False
        ) # get the right hand where you want it

        self.left_hand.rect.center = self.inventory_sprite.rect.center + vec(
            (-self.inventory_sprite.rect.center[0]//2, 0)
        )
        self.right_hand.rect.center = self.inventory_sprite.rect.center + vec(
            (self.inventory_sprite.rect.center[0]//2, 0)
        )
        self.left_glyph.rect.midtop = self.left_hand.rect.midbottom
        self.right_glyph.rect.midtop = self.right_hand.rect.midbottom
        
        self.marker.rect.center = self.inventory_sprite.rect.center

        slots = self.init.get("slots")
        if slots:
            for i in range(slots):
                self.add_slot()

        items = self.init.get("items")
        if items:
            for item_init in items:
                instance = Item(**item_init)
                self.add_item(instance)


    def update(self):
        if self.scene is not self.parent.scene:
            self.scene = self.parent.scene

        input_actions, held = self.parent.scene.game.input.get()
        new_actions = self.parent.scene.game.input.new_actions()

        if "START" in new_actions:
            self.toggle()
        
        if not any([inp in LEFT_STICK_AX for inp, _ in input_actions]):
            self.marker.rect.center = self.inventory_sprite.rect.center
        
        slot_index = self.get_selected_item_slot()
        if slot_index is not None:
            slot_rect = self.slot_sprites.sprites()[slot_index].rect
            self.marker.rect.center = slot_rect.center
        
        # TODO -3- refine as we go but this code is temporary and was just to get a hud going
        self.parent.scene.hud.add(self.life_meter)
        amount_to_block_out = self.hp / self.hp_max
        surface = pg.Surface(self.life_meter.rect.size, flags=pg.SRCALPHA)
        surface.fill((0,0,0,255))
        pos = (
            vec(self.life_meter.rect.size).elementwise()
            * vec([amount_to_block_out ,0])
        )
        life_mask = pg.mask.from_surface(self.life_meter_decal.image)
        overlap = life_mask.overlap_mask(pg.mask.from_surface(surface), pos)
        black_surface = overlap.to_surface(
            setcolor=(0,0,0, 255), unsetcolor=(0, 0, 0, 0)
        )
        self.life_meter.image.blit(self.life_meter_decal.image, (0,0))
        self.life_meter.image.blit(black_surface, (0,0))#, pos)
        ###

        money_render = pg.Surface(
            vec(self.coin_decal.rect.size).elementwise() * vec((4, 1)),
            flags=pg.SRCALPHA
        )
        money_render.blit(self.coin_decal.image, (0,0))
        rendered_text = self.money_text.render(
            f"{self.money:03}", True, (255,255,255)
        )
        money_render.blit(rendered_text, (self.coin_decal.rect.size[0], 0))
        self.money_decal.set_image(money_render)
        self.parent.scene.hud.add(self.money_decal)
        self.money_decal.rect.bottomright = (
            self.scene.game.draw_surface.get_rect().bottomright + vec((16,-5))
        )
        
        if self.hp <= 0:
            self.parent.kill()
            self.parent.scene.deconstruct(save_scene=False)
            self.parent.scene.game.load_scene(
                yaml_path="./assets/scene/game_over.yaml"
            )

        if not input_actions: return
        actions, values = list(map(list, zip(*input_actions)))

        self.apply_left_stick(actions, values)
        self.apply_buttons(new_actions)

        
    def toggle(self):
        self.scene.paused = not self.scene.paused
        self.active = not self.active
        toggle_state = (
            self.parent.scene.hud.add 
            if self.active else 
            self.parent.scene.hud.remove
        )
        # ORDER MATTERS first we do the backpack and hands
        for sprite in [
            self.inventory_sprite, 
            self.left_hand, 
            self.right_hand,
            self.left_glyph,
            self.right_glyph
        ]:
            toggle_state(sprite)

        # then we do the slots
        n_slots = len([slot for slot in self.slots if slot])
        for i, slot_sprite in enumerate(self.slot_sprites.sprites()):
            toggle_state(slot_sprite)
            slot_sprite.rect.center = (
                vec(self.inventory_sprite.rect.center) + 
                (vec(Compass.unit_vector(Compass.UP)) * 
                    self.inventory_sprite.image.get_height()
                ).rotate(i / n_slots * 360)
            )
        # then the sprites over the slots
        for slot_sprite, item in zip(self.slot_sprites.sprites(), self.slots):
            toggle_state(item)
            item.rect.center = slot_sprite.rect.center

        # finally the hand items and the marker goes LAST
        for sprite in [self.left_item, self.right_item, self.marker]:
            toggle_state(sprite)
        
        if not self.active:
            self.marker.rect.center = self.inventory_sprite.rect.center


    def change_money(self, amount:int) -> int|None:
        new_amount = self.money + amount
        if new_amount < 0:
            return None # this cannot happen

        if new_amount > self.max_money:
            new_amount = self.max_money
        
        self.money = new_amount
        return new_amount


    def change_health(self, amount:int) -> int:
        self.hp = self.hp + amount if self.hp + amount > 0 else 0
        self.hp = self.hp if self.hp < self.hp_max else self.hp_max
        return self.hp

    
    def serialize(self):
        n_slots = len(self.slots)
        items = [
            sprite.init 
            for sprite in ([self.left_item, self.right_item] + self.slots)
            if sprite.id != "empty"
        ]
        return (self.init | {
            "id": self.id,
            "type": "Inventory",
            "money": self.money,
            "max_money": self.max_money,
            "hp": self.hp,
            "hp_max": self.hp_max,
            "slots": n_slots,
            "items": items
        })


    def add_slot(self):
        if len(self.slots) >= N_SLOTS: return None          

        self.slots.append(self.empty_item())
        new_slot = Decal(**{
            "parent": self,
            "id": f"inventory_slot({len(self.slots)-1})",
            "scene": None,
            "image": "./assets/actor/inventory_screen/slot.png",
            "mask": None,
            "scale": INV_SCALE
        })
        self.slot_sprites.add(new_slot)
        new_slot.add(self.scene.all_nodes)
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
                
                self.slots[i] = item
                self.slots[i].rect.center = (
                    self.slot_sprites.sprites()[i].rect.center
                )
                return self.slots[i]
        
        return None


    def remove_item(self, id_:str) -> Item:
        """returns an empty item if it removed successfully None otherwise"""
        for i, slot in enumerate(self.slots):
            if slot.id == id_:
                self.slots[i] = self.empty_item()
                return self.slots[i]
        if self.left_item.id == id_:
            self.left_item = self.empty_item()
            return self.left_item
        if self.right_item.id == id_:
            self.right_item = self.empty_item()
            return self.right_item
        
        return None


    def get_selected_item_slot(self):
        indices = self.marker.rect.collidelistall(
            self.slot_sprites.sprites()
        )
        if not indices: return None
        return indices[0]


    def empty_item(self):
        return Item(**{
            'parent': self,
            'id' : 'empty',
            "image" : "./assets/block/null.png",
            "scene" : None,
            'mask' : None,
            'action': None
        })


    def select(self, hand:str) -> Item:
        i_select = self.get_selected_item_slot()
        if i_select is None: # just swap hands
            self.right_item, self.left_item = self.left_item, self.right_item
            self.right_item.rect.center = self.right_hand.rect.center
            self.left_item.rect.center = self.left_hand.rect.center
            return None

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


    def contains(self, id_:str) -> bool:
        
        for item in [self.left_item, self.right_item] + self.slots:
            
            if item and item.id == id_:
                return True
        return False


    # def apply_right_stick(self, actions, values):
    #     # activate inventory
    #     vector = vec([0,0])
    #     for direction in RIGHT_STICK_AX:
    #         if not (direction in actions): continue
    #         value = values[actions.index(direction)]
    #         # this line is for moving the right stick to activate the menu
    #         # if not self.active: self.toggle()
    #         multiplier = abs(value) if value else 1.0
    #         vector += (
    #             Compass.vector(direction[2:]) * 
    #             self.inventory_sprite.image.get_height() * 
    #             multiplier
    #         )

    #     self.marker.rect.center = (
    #         self.inventory_sprite.rect.center + 
    #         vector
    #     )


    def apply_left_stick(self, actions, values):
        # activate inventory
        vector = vec([0,0])
        for direction in LEFT_STICK_AX:
            if not (direction in actions): continue
            value = values[actions.index(direction)]
            # this line is for moving the right stick to activate the menu
            # if not self.active: self.toggle()
            multiplier = abs(value) if value else 1.0
            vector += (
                Compass.vector(direction) * 
                self.inventory_sprite.image.get_height() * 
                multiplier
            )

        self.marker.rect.center = (
            self.inventory_sprite.rect.center + 
            vector
        )


    def apply_buttons(self, new_actions):

        if (LEFT_HAND_BUTTON in new_actions):
            if self.active:
                self.select("LEFT")
            elif self.left_item.id != EMPTY:
                self.animation_id = self.left_item.action
                if self.animation_id:
                    self.state = self.animation_id
        
        if (RIGHT_HAND_BUTTON in new_actions):
            if self.active:
                self.select("RIGHT")
            elif self.right_item.id != EMPTY:
                self.animation_id = self.right_item.action
                if self.animation_id:
                    self.state = self.animation_id