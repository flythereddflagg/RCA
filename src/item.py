from .decal import Decal

class Item(Decal):
    def __init__(self, id_:str='empty', scene=None, image=None, action=None):
        self.id = id_
        if self.id == 'empty':
            self.sprite = None
            return
        super().__init__(**{
            "id": f"{self.id} - Item Sprite",
            "scene": scene,
            "image": image,
            "mask": None,
            "scale": 1
        })
        self.action = action
    
    def __repr__(self):
        return f"<Item - {self.id}>"

    def select(self):
        return self.action
