class Node():
    """Interface class for all in-game objects that have or manage sprites"""
    def __init__(self, scene, **options):
        self.scene = scene # Force all nodes to have a scene
        id_ = options.get('id')
        self.id = id_ if id_ else str(type(self)) + str(id(self))
        self.options = options


    def update(self):
        """
        This will be called every frame and allows for updates to the child
        node
        """
        raise NotImplementedError(
            "Interface method was called. Implement"
            f" the 'update' function in class {type(self)}"
        )
