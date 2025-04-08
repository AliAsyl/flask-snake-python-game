import random
from engine.core import GameObject, Rect2D, Vector2D

class Cat(GameObject):
    CAT_HITBOX_WIDTH = 64
    CAT_HITBOX_HEIGHT = 64
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, Cat.CAT_HITBOX_WIDTH, Cat.CAT_HITBOX_HEIGHT))
        self.collected_berries = 0
        self.collected_points = 0
        self.move_speed = 10
    def on_collision_detection(self, other):
        if isinstance(other, Berry):
            self.collected_berries += 1
            self.collected_points += other.points
            other.dispose()

class Berry(GameObject):
    BERRY_HITBOX_WIDTH = 32
    BERRY_HITBOX_HEIGHT = 32
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, Berry.BERRY_HITBOX_WIDTH, Berry.BERRY_HITBOX_HEIGHT))
        self.points = random.randint(10, 100)