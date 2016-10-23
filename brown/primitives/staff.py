from brown.utils import units
from brown.config import config
from brown.core import brown
from brown.core.path import Path
from brown.primitives.clef import Clef


class Staff:

    def __init__(self, x, y, length, staff_unit=None):
        self._x = x
        self._y = y
        self._line_count = 5
        self._length = length
        if staff_unit:
            self.staff_unit = staff_unit * units.mm
        else:
            self.staff_unit = config.DEFAULT_STAFF_UNIT * units.mm
        self._contents = []
        self.grob = Path(self.x, self.y)
        # Draw the staff lines
        for i in range(self.line_count):
            self.grob.move_to(0, i * self.staff_unit)
            self.grob.line_to(self.length, i * self.staff_unit)
        # TODO: More fully implement arbitrary numbers of staff lines

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """float: x coordinate of the left side of the staff"""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """float: y coordinate of the left side of the staff"""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def length(self):
        """float: length coordinate of the left side of the staff"""
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def height(self):
        """float: The height of the staff in pixels, from top to bottom line."""
        return (self.line_count - 1) * self.staff_unit

    @property
    def line_count(self):
        """int: The number of lines in the staff"""
        return self._line_count

    @property
    def contents(self):
        """list[StaffObject]: A list of staff objects belonging to the staff"""
        return self._contents

    ######## PRIVATE METHODS ########

    def _register_staff_object(self, staff_object):
        """Add a StaffObject to `self.contents`.

        Args:
            staff_object (StaffObject): The object to add to `self.contents`

        Warning:
            This does not set `staff_object.staff` to self"""
        self._contents.append(staff_object)
        staff_object.staff = self

    ######## PUBLIC METHODS ########

    def active_clef_at(self, position_x):
        """Find and return the active clef at a given point.

        Returns: Clef
        """
        # TODO: Find a more efficient way to quickly look up contents by type
        clefs_before = [item for item in self.contents
                        if isinstance(item, Clef) and
                        item.position_x <= position_x]
        return max(clefs_before, key=lambda c: c.position_x, default=None)

    def middle_c_at(self, position_x):
        """Find the vertical staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c. If no clef is present, treble is assumed.

        Returns:
            int: A vertical staff position, where 0 means the center
            line or space of the staff, higher numbers mean higher positions,
            and lower numbers mean lower positions.
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            # Assume treble
            return -6
        else:
            return clef.middle_c_staff_position

    def natural_midi_number_of_top_line_at(self, position_x):
        """Find the natural midi pitch class of the top line at a given point.

        Looks for clefs and other transposing modifiers to determine
        the this value. If no clef is present, treble is assumed.

        Returns an `int` midi pitch number.
        """
        # TODO: This currently assumes treble clef
        return 77

    def render(self):
        """Render the staff.

        Returns: None
        """
        self.grob.render()
