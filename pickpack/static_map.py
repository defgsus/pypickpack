

class StaticMap:

    """
    Map of the world in a particular state.
    """

    class Tiles:
        EMPTY = 0
        WALL = 1

    def __init__(self):
        self.map = []
        self.width = 0
        self.height = 0

    def init(self, width, height):
        self.width = width
        self.height = height
        self.map = [
            [self.Tiles.EMPTY] * self.width
            for i in range(self.height)
        ]
