import pygame as pg


class Node(pg.sprite.Sprite):
    """Interface class for all in-game objects that have or manage sprites"""
    def __init__(
                self, 
                scene, 
                parent:'Node'=None, 
                children:list['Node']=None, 
                **options
    ):
        super().__init__()
        self.scene = scene # Force all nodes to have a scene
        id_ = options.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.options = options
        self.parent = parent
        self.children = None if children is None else pg.sprite.Group(*children)


    def update(self):
        """
        This will be called every frame and allows for updates to the child
        node
        """
        raise NotImplementedError(
            "Interface method was called. Implement"
            f" the 'update' function in class {type(self)}"
        )

