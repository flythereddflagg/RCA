class Node():
    """Interface class for all in-game objects"""
    def __init__(self, scene):
        """
        Defined to promise that there will be a reference to a 
        parent 'scene' object given
        """
        raise NotImplementedError(
            "Interface method was called. Implement"
            f" the '__init__' function in class {type(self)}"
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