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
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def equals(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        raise TypeError("Can only compare Vector2D with other Vector2D")

Vector2D.UP = Vector2D(0, 1)
Vector2D.DOWN = Vector2D(0, -1)
Vector2D.RIGHT = Vector2D(1, 0)
Vector2D.LEFT = Vector2D(-1, 0)

class Rect2D:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height

    def intersects(self, other):
        return not (
            self.position.x + self.width <= other.position.x or
            self.position.x >= other.position.x + other.width or
            self.position.y + self.height <= other.position.y or
            self.position.y >= other.position.y + other.height
        )
    def is_inner_rect(self, other):
        return (
            other.position.x >= self.position.x and
            other.position.y >= self.position.y and
            other.position.x + other.width <= self.position.x + self.width and
            other.position.y + other.height <= self.position.y + self.height
        )
    def __str__(self):
        return f"[Rect@{self.position}:{self.width}x{self.height}]"
    def copy(self):
        return Rect2D(Vector2D(self.position.x, self.position.y), self.width, self.height)

class GameObject:
    GAME_OBJECTS = []
    def __init__(self, hitbox):
        self.hitbox = hitbox
        GameObject.GAME_OBJECTS.append(self)

    def on_collision_detection(self, collided_with):
        pass

    def move_and_collide(self, direction, speed=1):
        for go in GameObject.GAME_OBJECTS:
            if go != self and go.hitbox.intersects(self.hitbox):
                print(f"!!>>> self: {self}, {self.hitbox}| go: {go}, {go.hitbox}")
                go.on_collision_detection(self)
                self.on_collision_detection(go)
        self.hitbox.position += direction * speed

    def dispose(self):
        if self in GameObject.GAME_OBJECTS:
            GameObject.GAME_OBJECTS.remove(self)