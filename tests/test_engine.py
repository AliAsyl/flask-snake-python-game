import pytest
from game_engine.engine import move_object, check_collision, is_within_bounds


def test_move_object_up():
    assert move_object((5, 5), "up") == (5, 4)

def test_move_object_invalid_direction():
    with pytest.raises(ValueError):
        move_object((0, 0), "jump")

def test_move_object_at_origin():
    assert move_object((0, 0), "right") == (1, 0)

# Tests for check_collision

def test_check_collision_true():
    assert check_collision((2, 2), (2, 2)) == True

def test_check_collision_false():
    assert check_collision((2, 2), (3, 3)) == False

# Tests for is_within_bounds

def test_is_within_bounds_inside():
    assert is_within_bounds((3, 3), (10, 10)) == True

def test_is_within_bounds_on_edge():
    assert is_within_bounds((9, 9), (10, 10)) == True

def test_is_within_bounds_outside():
    assert is_within_bounds((10, 10), (10, 10)) == False

def test_is_within_bounds_negative():
    assert is_within_bounds((-1, 5), (10, 10)) == False