import random
from engine.core import GameObject, Rect2D, Vector2D
import statics

class Tail(GameObject):
    def __init__(self, position, visible=True):
        super().__init__(Rect2D(position, 1, 1))
        self.visible = visible

class Cat(GameObject):
    def __init__(self, start_pos, berries_to_collect):
        super().__init__(Rect2D(start_pos, 1, 1))
        self.move_direction = Vector2D.RIGHT
        self.collected_berries = 0
        self.collected_points = 0
        self.berries_to_collect = berries_to_collect
        self.tail = []


    def move(self, board):
        future_hitbox = self.hitbox.copy()
        future_hitbox.position += self.move_direction
        if board.is_inner_rect(future_hitbox):
            last_head_position = self.hitbox.copy().position

            self.move_and_collide(self.move_direction)
            for i in range(len(self.tail) - 1,-1,-1):
                if i == 0:
                    self.tail[i].hitbox.position = last_head_position
                else:
                    self.tail[i].hitbox.position = self.tail[i - 1].hitbox.position

    def on_collision_detection(self, other):
        if isinstance(other, Berry):
            self.collected_berries += 1
            self.collected_points += other.points
            self.tail.append(Tail(self.hitbox.copy().position, False))
            statics.GAME_OVER = (self.collected_berries >= self.berries_to_collect) and self.berries_to_collect != 0
        elif isinstance(other, Tail):
            if not(other.visible):
                other.visible = True
                return
            statics.GAME_RUNNING = False
            statics.GAME_OVER = True

class Berry(GameObject):
    def __init__(self, start_pos):
        super().__init__(Rect2D(start_pos, 1, 1))
        self.points = random.randint(10, 100)
    
    def on_collision_detection(self, collided_with):
        if isinstance(collided_with, Cat):
            self.dispose()
            
            Berry.spawn_new_berry()
            
    
    @staticmethod
    def spawn_new_berry():
        new_berry_position = None

        while new_berry_position is None:
            new_berry_position = Vector2D(
                random.randint(0, statics.SCREEN_RECT.width - 1),
                random.randint(0, statics.SCREEN_RECT.height - 1)
            )
            for go in GameObject.GAME_OBJECTS:
                if new_berry_position.equals(go.hitbox.position):
                    new_berry_position = None
                    break
        
        Berry(new_berry_position)