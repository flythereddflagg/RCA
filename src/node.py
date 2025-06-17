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
                scene, 
                parent:'Node'=None, 
                children:list[dict]=None, 
                **options
    ):
        super().__init__()
        self.scene = scene # Force all nodes to have a scene
        id_ = options.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.options = options
        self.parent = parent
        if children:
            for child in children:
                child['parent'] = self
        self.children = (
            None 
            if children is None 
            else pg.sprite.Group(*[
                node_from_dict(self.scene, child)
                for child in children
            ])
        )


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

    
    def __getattr__(self, name):
        return self.child_by_id(name)
    
    #TODO add code here that implments adding and killing children
