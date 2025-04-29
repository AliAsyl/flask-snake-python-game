import pytest
from engine.core import Vector2D, Rect2D, GameObject

def test_addition():
    v1 = Vector2D(1, 2)
    v2 = Vector2D(3, 4)
    result = v1 + v2
    assert result.x == 4
    assert result.y == 6

def test_scalar_multiplication():
    v = Vector2D(2, -1)
    result = v * 3
    assert result.x == 6
    assert result.y == -3

def test_reverse_multiplication():
    v = Vector2D(4, 5)
    result = 2 * v
    assert result.x == 8
    assert result.y == 10

def test_invalid_addition():
    v = Vector2D(1, 1)
    with pytest.raises(TypeError):
        _ = v + 5

def test_invalid_multiplication():
    v = Vector2D(1, 1)
    with pytest.raises(TypeError):
        _ = v * "not a number"

def test_vector_equality_same_values():
    v1 = Vector2D(3, 4)
    v2 = Vector2D(3, 4)
    assert v1.equals(v2)

def test_vector_equality_different_values():
    v1 = Vector2D(3, 4)
    v2 = Vector2D(4, 3)
    assert not(v1.equals(v2))

def test_vector_equality_different_type():
    v = Vector2D(1, 2)
    with pytest.raises(TypeError):
        _ = v.equals((1, 2))



def test_intersects_overlap():
    r1 = Rect2D(Vector2D(0, 0), 10, 10)
    r2 = Rect2D(Vector2D(5, 5), 10, 10)
    assert r1.intersects(r2) is True
    assert r2.intersects(r1) is True

def test_intersects_no_overlap():
    r1 = Rect2D(Vector2D(0, 0), 10, 10)
    r2 = Rect2D(Vector2D(20, 20), 5, 5)
    assert r1.intersects(r2) is False
    assert r2.intersects(r1) is False

def test_intersects_touching_edges():
    r1 = Rect2D(Vector2D(0, 0), 10, 10)
    r2 = Rect2D(Vector2D(10, 0), 10, 10)
    r3 = Rect2D(Vector2D(0, 10), 10, 10)
    assert r1.intersects(r2) is False
    assert r1.intersects(r3) is False

def test_intersects_inside():
    outer = Rect2D(Vector2D(0, 0), 10, 10)
    inner = Rect2D(Vector2D(2, 2), 5, 5)
    assert outer.intersects(inner) is True
    assert inner.intersects(outer) is True

def test_intersects_same_rect():
    r = Rect2D(Vector2D(3, 3), 4, 4)
    assert r.intersects(r) is True

def test_is_inner_rect_true():
    outer = Rect2D(Vector2D(0, 0), 100, 100)
    inner = Rect2D(Vector2D(10, 10), 20, 20)
    assert outer.is_inner_rect(inner) is True

def test_is_inner_rect_false_outside():
    outer = Rect2D(Vector2D(0, 0), 100, 100)
    outside = Rect2D(Vector2D(110, 110), 10, 10)
    assert outer.is_inner_rect(outside) is False

def test_is_inner_rect_false_partially_out():
    outer = Rect2D(Vector2D(0, 0), 100, 100)
    partial = Rect2D(Vector2D(90, 90), 20, 20)
    assert outer.is_inner_rect(partial) is False

def test_is_inner_rect_equal_size():
    outer = Rect2D(Vector2D(0, 0), 100, 100)
    same = Rect2D(Vector2D(0, 0), 100, 100)
    assert outer.is_inner_rect(same) is True

from engine.core import Rect2D, Vector2D

def test_copy_rect_returns_new_instance():
    original = Rect2D(Vector2D(10, 20), 100, 50)
    copy = original.copy()

    assert isinstance(copy, Rect2D)
    assert copy is not original
    assert copy.position is not original.position

def test_copy_rect_has_same_values():
    original = Rect2D(Vector2D(10, 20), 100, 50)
    copy = original.copy()

    assert copy.position.equals(Vector2D(10, 20))
    assert copy.width == 100
    assert copy.height == 50

def test_modifying_copy_does_not_affect_original():
    original = Rect2D(Vector2D(10, 20), 100, 50)
    copy = original.copy()
    copy.position.x = 999
    copy.width = 1
    copy.height = 1

    # Original should remain unchanged
    assert original.position.equals(Vector2D(10, 20))
    assert original.width == 100
    assert original.height == 50


class _TestGameObject(GameObject):
    def __init__(self, hitbox):
        super().__init__(hitbox)
        self.collisions = []

    def on_collision_detection(self, collided_with):
        self.collisions.append(collided_with)

@pytest.fixture(autouse=True)
def clear_game_objects():
    GameObject.GAME_OBJECTS.clear()

def test_moves_without_collision():
    obj = _TestGameObject(Rect2D(Vector2D(0, 0), 10, 10))

    obj.move_and_collide(Vector2D.RIGHT, speed=5)

    assert obj.hitbox.position.equals(Vector2D(5, 0))

def test_movement_on_collision():
    obj1 = _TestGameObject(Rect2D(Vector2D(0, 0), 10, 10))
    obj2 = _TestGameObject(Rect2D(Vector2D(5, 0), 10, 10))

    obj1.move_and_collide(Vector2D.RIGHT, speed=5)

    assert obj1.hitbox.position.equals(Vector2D(5, 0))

    assert obj2 in obj1.collisions
    assert obj1 in obj2.collisions

def test_dispose_removes_object():
    obj = _TestGameObject(Rect2D(Vector2D(0, 0), 10, 10))
    assert obj in GameObject.GAME_OBJECTS

    obj.dispose()
    assert obj not in GameObject.GAME_OBJECTS

def test_multiple_steps_movement():
    obj = _TestGameObject(Rect2D(Vector2D(0, 0), 5, 5))

    obj.move_and_collide(Vector2D.RIGHT, speed=2)
    obj.move_and_collide(Vector2D.DOWN, speed=3)

    assert obj.hitbox.position.equals(Vector2D(2, -3))
