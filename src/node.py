import string

import pygame as pg

from .tools import class_from_str, load_yaml

INHERIT_KEY = "_inherit_"
MISSING_TYPE = "<MISSING TYPE>"

def node_from_dict(scene:'.scene.Scene', node_init:dict) -> 'Node': 
    yaml = node_init.get("yaml")
    if yaml: # overwrite the data in yaml with the node_init 
        node_init = load_yaml(yaml) | node_init
    parent = node_init.pop("parent", None)
    class_str = node_init.get('type', MISSING_TYPE)
    if class_str == MISSING_TYPE:
        raise TypeError(f"Missing Type - {node_init}")
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
        parent_id = parent.id + "_" if parent else ""
        self.id = init.get(
            'id', 
            (
                parent_id 
                + str(type(self)).strip("<>'\"").split('.')[-1] 
                + str(id(self) % 10000))
        )
        self.init = init
        self.parent = parent
        if self.parent:
            for key, val in self.init.items():
                if val == INHERIT_KEY:
                    self.init[key] = self.parent.init.get(key)
        self.sprite = None
        # not a pg.sprite.Group so it is not affected by sprite.kill
        self.children = [] 
        children:list[dict] = init.get("children")
        if children:                
            for child in children:
                self.add_child(child)
        self.setup()


    def add_child(self, child:'Node|dict'):
        if isinstance(child, dict):
            child['parent'] = self
            node = node_from_dict(self.scene, child)
        elif isinstance(child, Node):
            child.parent = self
            node = child
        else:
            raise Exception(
                "Invalid child supplied. Must be existing node or node init dict"
            )

        self.children.append(node)
        node.scene = self.scene
        setattr(self, node.id, node)


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
                for sprite in self.children 
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
            for child in self.children:
                child.kill()

        super().kill()

    def __repr__(self):
        return f"<{str(str(type(self)).split('\'')[1])} - {self.id}>"

    
    def get_init(self):
        # NOTE function is recursive
        """returns the current init data to recreate the sprite from scratch"""
        init = {**self.init}
        init["type"] = type(self).__name__
        if "active" in init.keys(): # TODO -2- decide how this should work. Is default behavior to inherit active from parent?
            init["active"] = self in self.scene.active_nodes
        init["groups"] = self.scene.node_in_groups(self)
        init["groups"] = list(set(init["groups"]))
        if self.sprite:
            if self.sprite in self.scene.hud:
                init["start"] = list(self.sprite.rect.topleft)
            else:
                pass
                # init["start"] = list(self.scene.get_bg_pos(self.sprite.rect.topleft))
        if self.children:
            # rewrite children fully
            init["children"] = []
            for child in self.children:
                init["children"].append(child.get_init())
        return init
