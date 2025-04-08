import pytest
from engine.core import Vector2D, Rect2D

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
    assert r1.intersects(r2) is False  # Touching side
    assert r1.intersects(r3) is False  # Touching bottom

def test_intersects_inside():
    outer = Rect2D(Vector2D(0, 0), 10, 10)
    inner = Rect2D(Vector2D(2, 2), 5, 5)
    assert outer.intersects(inner) is True
    assert inner.intersects(outer) is True

def test_intersects_same_rect():
    r = Rect2D(Vector2D(3, 3), 4, 4)
    assert r.intersects(r) is True