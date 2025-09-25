import pygame as pg

from .tools import class_from_str, load_yaml

INHERIT_KEY = "_inherit_"

def node_from_dict(scene:'.scene.Scene', node_init:dict) -> 'Node': 
    yaml = node_init.get("yaml")
    if yaml: # overwrite the data in yaml with the node_init 
        node_init = load_yaml(yaml) | node_init
    parent = node_init.pop("parent", None)
    class_str = node_init.get('type')
    node = class_from_str(class_str)(scene=scene, parent=parent, **node_init)
    return node


class Node(pg.sprite.Sprite):
    """Interface class for all in-game objects that have or manage sprites"""
    def __init__(
                self,
                scene:'.scene.Scene'=None,
                parent:'.node.Node'=None,
                **init
    ):
        super().__init__()
        self.scene = scene
        id_ = init.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.init = init
        self.parent = parent
        if self.parent:
            for key, val in self.init.items():
                if val == INHERIT_KEY:
                    self.init[key] = self.parent.init.get(key)
        self.sprite = None
        self.children = pg.sprite.Group()
        children:list[dict] = init.get("children")
        if children:                
            for child in children:
                child['parent'] = self
                node = node_from_dict(self.scene, child)
                self.children.add(node)
                setattr(self, node.id, node)
        self.setup()


    def require_attr(self, *names:str, types=None):
        if types:
            names = zip(names, types)
        for name in names:
            if types:
                name, type_ = name
            else:
                type_ = None
            object_ = self.init.get(name)
            assert object_,\
                f"Required param '{name}' not provided to Node {str(self)}"
            if type_:
                assert isinstance(object_, type_),\
                    f"Required param '{name}' in Node {str(self)} "\
                    f"has type '{type(object_)}', expected {type_}"

    
    def setup(self):
        """
        Optional to implement in children but replaces the need
        for complicated call signatures ahd helps to serialize 
        objects
        """
        pass
    
    
    def deconstruct(self):
        """
        Called on scene deconstruction. May be overriden to
        do specific things when scenes deconstruct.
        """
        pass
        

    def signal(self, *args, **init):
        if self.parent: self.parent.signal(*args, **init)


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

    def __repr__(self):
        return f"<{str(str(type(self)).split('\'')[1])} - {self.id}>"
