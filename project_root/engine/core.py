class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector2D to Vector2D")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise TypeError("Can only multiply Vector2D by a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)


class Rect2D:
    def __init__(self, position, width, height):
        self.position = position  # Vector2D
        self.width = width
        self.height = height

    def intersects(self, other):
        return not (
            self.position.x + self.width <= other.position.x or
            self.position.x >= other.position.x + other.width or
            self.position.y + self.height <= other.position.y or
            self.position.y >= other.position.y + other.height
        )

    
