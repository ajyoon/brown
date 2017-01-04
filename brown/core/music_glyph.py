from brown.core import brown
from brown.core.glyph import Glyph
from brown.core.music_font import MusicFont
from brown.primitives.staff_object import StaffObject
from brown.utils.rect import Rect
from brown.utils.point import Point
from brown.utils.units import convert_all_to_unit


class MusicGlyph(Glyph, StaffObject):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.

    Unlike a Glyph, the text of a MusicGlyph may be passed either as a unicode
    character or as its corresponding canonical SMuFL name.
    """

    def __init__(self, pos, canonical_name, font=None, parent=None):
        if font is None:
            font = brown.music_font
        # type check font is MusicFont before sending to init?
        self._canonical_name = canonical_name
        codepoint = font.glyph_info(self.canonical_name)['codepoint']
        Glyph.__init__(self, pos, codepoint, font, parent)
        StaffObject.__init__(self, parent)
        self._generate_glyph_info()
        from pprint import pprint;pprint(self.glyph_info)

    ######## PUBLIC PROPERTIES ########n

    @property
    def canonical_name(self):
        """str: The canonical name of the glyph"""
        return self._canonical_name

    @property
    def glyph_info(self):
        """dict: The aggregated SMuFL metadata for this glyph"""
        try:
            return self._glyph_info
        except AttributeError:
            self._generate_glyph_info()
            return self._glyph_info

    @property
    def font(self):
        """MusicFont: The glyph music font."""
        return self._font

    @font.setter
    def font(self, value):
        # TODO: Code below is redundant with super,
        #       find a way to use inheritance here
        if not isinstance(value, MusicFont):
            raise TypeError('MusicGlyph.font must be a MusicFont')
        self._font = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _bounding_rect(self):
        """Rect: The bounding rect override for this glyph."""
        x = self.glyph_info['glyphBBox']['bBoxSW'][0]
        y = self.glyph_info['glyphBBox']['bBoxNE'][1]
        w = self.glyph_info['glyphBBox']['bBoxNE'][0] - x
        h = (self.glyph_info['glyphBBox']['bBoxSW'][1] - y) * (-1)
        return Rect(x, y, w, h)

    @property
    def _origin_offset(self):
        """Point: The origin offset override for this glyph."""
        # TODO
        return None

    ######## PRIVATE METHODS ########

    def _generate_glyph_info(self):
        """Find and generate SMuFL metadata for the glyph.

        This converts all numeric measurements to real StaffUnit values.

        Returns:
            dict: The aggregated SMuFL metadata for this glyph
        """
        self._glyph_info = self.font.glyph_info(self.canonical_name)
        convert_all_to_unit(self._glyph_info, self.staff.unit)
