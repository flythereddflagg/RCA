class Item():
    def __init__(self, id_:str):
        self.id = id_
    
    def __repr__(self):
        return f"<Item - {self.id}>"
