import unittest
import pytest

from brown.utils.point import Point

from brown.utils.base_unit import BaseUnit
from brown.utils.mm import Mm


class TestPoint(unittest.TestCase):

    def test_init_with_pair(self):
        test_point = Point(5, 6)
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_init_with_2_tuple(self):
        test_point = Point((5, 6))
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_init_with_existing_Point(self):
        existing_point = Point(5, 6)
        test_point = Point(existing_point)
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_init_with_unit(self):
        test_point = Point.with_unit(5, 6, unit_class=BaseUnit)
        assert(isinstance(test_point.x, BaseUnit))
        assert(isinstance(test_point.y, BaseUnit))
        assert(test_point.x == BaseUnit(5))
        assert(test_point.y == BaseUnit(6))

    def test_with_unit_fails_if_unit_class_not_set(self):
        with pytest.raises(TypeError):
            Point.with_unit(5, 6)

    def test_to_unit_from_int(self):
        test_point = Point(5, 6)
        test_point.to_unit(BaseUnit)
        assert(isinstance(test_point.x, BaseUnit))
        assert(isinstance(test_point.y, BaseUnit))
        assert(test_point.x == BaseUnit(5))
        assert(test_point.y == BaseUnit(6))

    def test_to_unit_from_other_unit(self):
        test_point = Point(BaseUnit(1), BaseUnit(2))
        test_point.to_unit(Mm)
        assert(isinstance(test_point.x, Mm))
        assert(isinstance(test_point.y, Mm))
        self.assertAlmostEqual(test_point.x, Mm(BaseUnit(1)))
        self.assertAlmostEqual(test_point.y, Mm(BaseUnit(2)))

    def test_iteration(self):
        test_point = Point(5, 6)
        result = []
        for dimension in test_point:
            result.append(dimension)
        assert(result == [5, 6])

    def test_indexing(self):
        test_point = Point(5, 6)
        assert(test_point[0] == 5)
        assert(test_point[1] == 6)

    def test_indexing_with_invalid_raises_IndexError(self):
        test_point = Point(5, 6)
        with pytest.raises(IndexError):
            test_point[3]
        with pytest.raises(IndexError):
            test_point[-1]
        with pytest.raises(TypeError):
            test_point['nonsense index']
