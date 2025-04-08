import pytest
from engine.core import Vector2D

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

