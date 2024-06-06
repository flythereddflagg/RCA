class Node():
    """Interface class for all in-game objects"""
    def __init__(self, scene, **kwargs):
        self.scene = scene # Force all nodes to have a scene


    def update(self):
        """
        This will be called every frame and allows for updates to the child
        node
        """
        raise NotImplementedError(
            "Interface method was called. Implement"
            f" the 'update' function in class {type(self)}"
        )
