import pygame as pg

from .tools import class_from_str, load_yaml

def node_from_dict(scene:'.scene.Scene', node_init:dict) -> 'Node':
    node_init['scene'] = scene
    yaml = node_init.get("yaml")
    if yaml: node_init = {**node_init, **load_yaml(yaml)}
    class_str = node_init['type']
    node = class_from_str(class_str)(**node_init)
    return node


class Node(pg.sprite.Sprite):
    """Interface class for all in-game objects that have or manage sprites"""
    def __init__(
                self, 
                scene=None,
                parent:'Node'=None, 
                children:list[dict]=None, 
                **init
    ):
        super().__init__()
        self.scene = scene
        id_ = init.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.init = init
        self.parent = parent
        self.sprite = None
        self.children = pg.sprite.Group()
        if children:                
            for child in children:
                child['parent'] = self
                node = node_from_dict(self.scene, child)
                self.children.add(node)
                setattr(self, node.id, node)



    def update(self):
        """
        This will be called every frame and allows for updates to the child
        node
        """
        raise NotImplementedError(
            "Interface method was called. Implement"
            f" the 'update' function in class {type(self)}"
        )


    def child_by_id(self, id_str:str) -> 'Node':
        if self.children:
            child = [
                sprite 
                for sprite in self.children.sprites() 
                if sprite.id == id_str
            ]
            if len(child) == 1:
                return child[0]
            elif len(child) > 1:
                raise ValueError(f"Multiple Children returned for ID {id_str}")
        
        return None # case len(child) == 0 or is an invalid value

    
    def kill(self):
        """
        if you kill a parent. Kill all children too.
        """
        if self.children:
            for child in self.children.sprites():
                child.kill()

        super().kill()

    #TODO add code here that implments adding children
    def __repr__(self):
        return f"<{str(str(type(self)).split('\'')[1])} - {self.id}>"
    
    def get_var_state(self):
        return vars(self)
