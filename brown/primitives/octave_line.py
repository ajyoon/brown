from brown.core.graphic_object import GraphicObject
from brown.core.object_group import ObjectGroup
from brown.core.music_text_object import MusicTextObject
from brown.core.music_char import MusicChar
from brown.core.path import Path
from brown.core.pen import Pen
from brown.primitives.staff_object import StaffObject
from brown.primitives.spanner import Spanner
from brown.utils.point import Point
from brown.utils.units import Unit, GraphicUnit
from brown.utils.stroke_pattern import StrokePattern


class OctaveLine(ObjectGroup, Spanner, StaffObject):

    """An octave indication with a dashed line.

    When placed in the context of a Staff, pitched content under the spanner
    is automatically transposed accordingly

    Supported octave indications are:
        - '15ma' (two octaves higher)
        - '8va' (one octave higher)
        - '8vb' (one octave lower)
        - '15mb' (two octaves lower)

    At the starting position the octave is written in text, followed by
    a dashed line ending in a small vertical hook pointing toward the staff.
    If the spanner goes across line breaks, the octave text is repeated
    in parenthesis at the line beginning.

    TODO: The dashed line portion of this spanner overlaps with the '8va' text.
          This is a nontrivial fix that may require implementing text
          background masking or a way to easily inject line continuation
          offsets for paths.
    """

    octaves = {
        '15ma': 2,
        '8va': 1,
        '8vb': -1,
        '15mb': -2
    }

    glyphs = {
        '15ma': 'quindicesimaAlta',
        '8va': 'ottavaAlta',
        '8vb': 'ottavaBassaVb',
        '15mb': 'quindicesimaBassaMb',
        '(': 'octaveParensLeft',
        ')': 'octaveParensRight'
    }

    def __init__(self,
                 start, start_parent,
                 stop_x, stop_parent=None,
                 indication='8va'):
        """
        Args:
            start (Point or tuple init args):
            start_parent (GraphicObject): An object either in a Staff or
                a staff itself. This object will become the line's parent.
            stop (Unit): The spanner end x position. The y position will be
                automatically calculated to be horizontal.
            stop_parent (GraphicObject): An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of `start_parent`. If omitted, the
                stop point is relative to the start point.
            indication (str): A valid octave indication.
                currently supported indications are:
                    - '15ma' (two octaves higher)
                    - '8va' (one octave higher)
                    - '8vb' (one octave lower)
                    - '15mb' (two octaves lower)
                The default value is '8va'.
        """
        ObjectGroup.__init__(self, start, start_parent)
        # NOTE: The logic/pattern used here to ensure a horizontal spanner
        #       will likely prove useful in other cases, warranting perhaps
        #       a general horizontal spanner pattern solution.
        #       Maybe a constructor like Spanner.horizontal(end_x, end_parent)
        if stop_parent:
            stop_y = self.frame.map_between_items_in_frame(stop_parent, self).y
        else:
            stop_y = GraphicUnit(0)
        Spanner.__init__(self, Point(stop_x, stop_y), stop_parent)
        StaffObject.__init__(self, self.parent)
        self.line_text = OctaveLine._OctaveLineText(
            # No offset relative to ObjectGroup
            pos=(GraphicUnit(0), GraphicUnit(0)),
            parent=self,
            length=self.length,
            indication=indication)

        # Vertically center the path relative to the text
        path_y = self.line_text._bounding_rect.height / -2
        self.line_path = Path(
            pos=(GraphicUnit(0), path_y),
            pen=Pen(
                thickness=self.staff.music_font.engraving_defaults[
                    'octaveLineThickness'],
                pattern=StrokePattern.DASH
            ),
            parent=self
        )
        # Drawn main line part
        self.line_path.line_to(self.end_pos.x, path_y, self.end_parent)
        pos_relative_to_staff = self.frame.map_between_items_in_frame(
            self.staff, self)
        # Draw end hook pointing toward the staff
        hook_direction = 1 if pos_relative_to_staff.y <= GraphicUnit(0) else -1
        self.line_path.line_to(self.end_pos.x,
                               (path_y
                                + self.staff.unit(0.75 * hook_direction)),
                               self.end_parent)

    class _OctaveLineText(MusicTextObject):
        """An octave text mark recurring at line beginnings with added parenthesis.

        This is a private class meant to be used exclusively in the context
        of an OctaveLine
        """

        def __init__(self, pos, parent, length, indication):
            """
            Args:
                pos (Point):
                parent (GraphicObject):
                length (Unit):
                indication (str): A valid octave indication.
                    Should be a valid entry in OctaveLine.glyphs.
            """
            MusicTextObject.__init__(self,
                                     pos,
                                     OctaveLine.glyphs[indication],
                                     parent)
            open_paren_char = MusicChar(self.font, OctaveLine.glyphs['('])
            close_paren_char = MusicChar(self.font, OctaveLine.glyphs[')'])
            self.parenthesized_text = (open_paren_char.codepoint
                                       + self.text
                                       + close_paren_char.codepoint)
            self._breakable_width = length

        ######## PUBLIC PROPERTIES ########

        @property
        def breakable_width(self):
            """Unit: The breakable width of the object.

            This is used to determine how and where rendering cuts should be made.
            """
            return self._breakable_width

        ######## PRIVATE METHODS ########

        def _render_before_break(self, local_start_x, start, stop):
            interface = self._interface_class(
                start,
                self.text,
                self.font._interface,
                origin_offset=self._origin_offset)
            interface.render()
            self.interfaces.add(interface)

        def _render_after_break(self, local_start_x, start, stop):
            interface = self._interface_class(
                start,
                self.parenthesized_text,
                self.font._interface,
                origin_offset=self._origin_offset)
            interface.render()
            self.interfaces.add(interface)

        def _render_spanning_continuation(self, local_start_x, start, stop):
            interface = self._interface_class(
                start,
                self.parenthesized_text,
                self.font._interface,
                origin_offset=self._origin_offset)
            interface.render()
            self.interfaces.add(interface)
