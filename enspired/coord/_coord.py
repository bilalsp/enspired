class Coord:
    """Represent a coordinate of old-format plan matrix."""

    def __init__(self, x: int, y: int) -> None:
        """Create a coordinate for plan-matrix cell.
        
        Args:
            x: x-coordinate
            y: y-coordinate
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "Coord({}, {})".format(self.x, self.y)

    def __eq__(self, coord):
      
        return self.x == coord.x and self.y == coord.y

    def __add__(self, coord):
        return Coord(self.x + coord.x, self.y + coord.y)

    def __sub__(self, coord):
        return Coord(self.x - coord.x, self.y - coord.y)
