import unittest

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.brush_pattern import BrushPattern
from neoscore.interface.brush_interface import BrushInterface
from neoscore.utils.color import Color


class TestBrush(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

    def test_init_with_hex_color(self):
        brush = Brush("#eeddcc")
        assert brush.color == Color(238, 221, 204, 255)

    def test_pattern_defaults_to_solid_color(self):
        brush = Brush("#ffffff")
        assert brush.pattern == BrushPattern.SOLID

    def test_init_with_pattern(self):
        brush = Brush("#ffffff", BrushPattern.DENSE_1)
        assert brush.pattern == BrushPattern.DENSE_1

    def test_from_existing(self):
        original = Brush(Color("#ffffff"), BrushPattern.DENSE_1)
        clone = Brush.from_existing(original)
        assert id(original) != id(clone)
        assert original.color == clone.color
        assert original.pattern == clone.pattern

    def test_interface_generation(self):
        brush = Brush(Color("#ffffff"), BrushPattern.DENSE_1)
        assert brush.interface == BrushInterface(Color("#ffffff"), BrushPattern.DENSE_1)

    def test_setters_update_interface(self):
        brush = Brush(Color("#000000"), BrushPattern.DENSE_1)
        brush.color = Color("#ffffff")
        assert brush.interface.color == Color("#ffffff")
        brush.pattern = BrushPattern.SOLID
        assert brush.interface.pattern == BrushPattern.SOLID
