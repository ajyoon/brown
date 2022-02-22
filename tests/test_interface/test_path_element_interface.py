import unittest

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.core.path_element_type import PathElementType
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.path_element_interface import PathElementInterface
from brown.interface.path_interface import PathInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.point import Point
from brown.utils.units import Unit

from ..helpers import assert_almost_equal


class TestPathElementInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.pen = PenInterface(
            Color("#000000"),
            Unit(0),
            PenPattern.SOLID,
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_init(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.line_to(Point(Unit(10), Unit(11)))
        qt_element = test_path.qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 1, 1)

        assert test_element.pos.x == Unit(10)
        assert test_element.pos.y == Unit(11)
        assert test_element.path_interface == test_path
        assert test_element.element_type == PathElementType.line_to
        assert test_element.index == 1
        assert test_element.qt_object == qt_element

    def test_is_move_to(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.move_to(Point(Unit(10), Unit(11)))
        qt_element = test_path.qt_path.elementAt(0)
        test_element = PathElementInterface(qt_element, test_path, 0, 0)
        assert test_element.element_type == PathElementType.move_to

    def test_is_line_to(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.line_to(Point(Unit(10), Unit(11)))
        qt_element = test_path.qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 0, 1)
        assert test_element.element_type == PathElementType.line_to

    def test_curves_and_control_points(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.cubic_to(
            Point(Unit(10), Unit(11)),
            Point(Unit(20), Unit(0)),
            Point(Unit(50), Unit(30)),
        )

        qt_element_1 = test_path.qt_path.elementAt(1)
        test_element_1 = PathElementInterface(qt_element_1, test_path, 0, 3)
        assert test_element_1.element_type == PathElementType.control_point

        qt_element_2 = test_path.qt_path.elementAt(2)
        test_element_2 = PathElementInterface(qt_element_2, test_path, 0, 3)
        assert test_element_2.element_type == PathElementType.control_point

        qt_element_3 = test_path.qt_path.elementAt(3)
        test_element_3 = PathElementInterface(qt_element_3, test_path, 0, 2)
        assert test_element_3.element_type == PathElementType.curve_to
