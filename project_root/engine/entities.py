import random
from engine.core import GameObject, Rect2D, Vector2D

class Cat(GameObject):
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, 64, 64))
        self.collected_berries = 0
        self.collected_points = 0
        self.move_speed = 10
    def on_collision_detection(self, other):
        if isinstance(other, Berry):
            self.collected_berries += 1
            self.collected_points += other.points
            other.dispose()

class Berry(GameObject):
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, 32, 32))
        self.points = random.randint(10, 100)