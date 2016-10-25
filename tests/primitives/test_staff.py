import unittest
import pytest

from brown.core import brown
from brown.config import config
from brown.utils import units
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef


class TestStaff(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_staff_pos_to_top_down(self):
        test_staff = Staff(0, 0, 100, line_count=5)
        # Center of staff
        assert(test_staff._staff_pos_to_top_down(0) == 4)
        # Above center
        assert(test_staff._staff_pos_to_top_down(1) == 3)
        assert(test_staff._staff_pos_to_top_down(4) == 0)
        assert(test_staff._staff_pos_to_top_down(5) == -1)
        assert(test_staff._staff_pos_to_top_down(12) == -8)
        # Below center
        assert(test_staff._staff_pos_to_top_down(-1) == 5)
        assert(test_staff._staff_pos_to_top_down(-4) == 8)
        assert(test_staff._staff_pos_to_top_down(-5) == 9)
        assert(test_staff._staff_pos_to_top_down(-12) == 16)

    def test_height(self):
        # 5 lines
        self.assertAlmostEqual(
            Staff(0, 0, 100, staff_unit=1.5, line_count=5).height, 6 * units.mm)
        self.assertAlmostEqual(
            Staff(0, 0, 100, staff_unit=1, line_count=5).height, 4 * units.mm)
        # 4 lines
        self.assertAlmostEqual(
            Staff(0, 0, 100, staff_unit=1.5, line_count=4).height, 4.5 * units.mm)
        self.assertAlmostEqual(
            Staff(0, 0, 100, staff_unit=1, line_count=4).height, 3 * units.mm)

    def test_active_clef_at_with_explicit_clefs(self):
        test_staff = Staff(0, 0, 100)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should have treble in effect
        assert(test_staff.active_clef_at(5) == test_treble_clef)
        # Test after bass clef goes into effect
        assert(test_staff.active_clef_at(15) == test_bass_clef)

    def test_active_clef_at_with_implicit_default_clef(self):
        test_staff = Staff(0, 0, 100)
        # No clef specified - should default to None (implicit treble)
        assert(test_staff.active_clef_at(5) is None)

    def test_middle_c_at_with_explicit_clefs(self):
        test_staff = Staff(0, 0, 100)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should be in treble mode
        assert(test_staff.middle_c_at(5) == -6)
        # Test after bass clef goes into effect
        assert(test_staff.middle_c_at(15) == 6)

    def test_middle_c_at_with_implicit_default_clef(self):
        test_staff = Staff(0, 0, 100)
        # No clef specified - should default to treble
        assert(test_staff.middle_c_at(5) == -6)

    def test_natural_midi_number_of_top_line_at_with_explicit_clefs(self):
        test_staff = Staff(0, 0, 100)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should be in treble mode
        assert(test_staff._natural_midi_number_of_top_line_at(5) == 77)
        # Test after bass clef goes into effect
        assert(test_staff._natural_midi_number_of_top_line_at(15) == 57)

    def test_natural_midi_number_of_top_line_at_with_implicit_default_clef(self):
        test_staff = Staff(0, 0, 100)
        # No clef specified - should default to treble
        assert(test_staff._natural_midi_number_of_top_line_at(5) == 77)

    def test_staff_pos_outside_staff_with_odd_line_count(self):
        test_staff_5 = Staff(0, 0, 100, line_count=5)
        assert(test_staff_5._staff_pos_outside_staff(0) is False)
        assert(test_staff_5._staff_pos_outside_staff(4) is False)
        assert(test_staff_5._staff_pos_outside_staff(-4) is False)
        assert(test_staff_5._staff_pos_outside_staff(5) is True)
        assert(test_staff_5._staff_pos_outside_staff(-5) is True)

    def test_staff_pos_outside_staff_with_even_line_count(self):
        test_staff_4 = Staff(0, 0, 100, line_count=4)
        assert(test_staff_4._staff_pos_outside_staff(0) is False)
        assert(test_staff_4._staff_pos_outside_staff(3) is False)
        assert(test_staff_4._staff_pos_outside_staff(-3) is False)
        assert(test_staff_4._staff_pos_outside_staff(4) is True)
        assert(test_staff_4._staff_pos_outside_staff(-4) is True)

    def test_position_needs_ledger_with_odd_line_count(self):
        test_staff_5 = Staff(0, 0, 100, line_count=5)
        assert(test_staff_5._position_needs_ledger(0) is False)
        assert(test_staff_5._position_needs_ledger(4) is False)
        assert(test_staff_5._position_needs_ledger(-4) is False)
        assert(test_staff_5._position_needs_ledger(6) is True)
        assert(test_staff_5._position_needs_ledger(-6) is True)
        assert(test_staff_5._position_needs_ledger(7) is False)
        assert(test_staff_5._position_needs_ledger(-7) is False)
        assert(test_staff_5._position_needs_ledger(8) is True)
        assert(test_staff_5._position_needs_ledger(-8) is True)

    def test_position_needs_ledger_with_even_line_count(self):
        test_staff_4 = Staff(0, 0, 100, line_count=4)
        assert(test_staff_4._position_needs_ledger(0) is False)
        assert(test_staff_4._position_needs_ledger(3) is False)
        assert(test_staff_4._position_needs_ledger(-3) is False)
        assert(test_staff_4._position_needs_ledger(4) is False)
        assert(test_staff_4._position_needs_ledger(-4) is False)
        assert(test_staff_4._position_needs_ledger(5) is True)
        assert(test_staff_4._position_needs_ledger(-5) is True)
        assert(test_staff_4._position_needs_ledger(6) is False)
        assert(test_staff_4._position_needs_ledger(-6) is False)
        assert(test_staff_4._position_needs_ledger(7) is True)
        assert(test_staff_4._position_needs_ledger(-7) is True)
