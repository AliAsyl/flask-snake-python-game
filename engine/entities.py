import random
from engine.core import GameObject, Rect2D, Vector2D

print([i for i in range(1 - 1, -1, -1)])

class Tail(GameObject):
    def __init__(self, position):
        super().__init__(Rect2D(position, 1, 1))

class Cat(GameObject):
    def __init__(self, start_pos, berries_to_collect):
        super().__init__(Rect2D(start_pos, 1, 1))
        self.move_direction = Vector2D.RIGHT
        self.collected_berries = 0
        self.collected_points = 0
        self.berries_to_collect = berries_to_collect
        self.tail = []
        self.last_tail_position = None


    def move(self, board):
        future_hitbox = self.hitbox.copy()
        future_hitbox.position += self.move_direction
        if board.is_inner_rect(future_hitbox):
            if len(self.tail) > 0:
                self.last_tail_position = self.tail[-1].hitbox.copy().position
                for i in range(len(self.tail) - 1, -1, -1):
                    if i == 0:
                        self.tail[0].hitbox.position = self.hitbox.copy().position
                    else:
                        self.tail[i - 1].hitbox.position = self.tail[i].hitbox.position
            else:
                self.last_tail_position = self.hitbox.copy().position
            self.move_and_collide(self.move_direction)

            return True
        return False

    def on_collision_detection(self, other):
        if isinstance(other, Berry):
            self.collected_berries += 1
            self.collected_points += other.points
            self.tail.append(self.last_tail_position)

            other.dispose()

class Berry(GameObject):
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, 1, 1))
        self.points = random.randint(10, 100)