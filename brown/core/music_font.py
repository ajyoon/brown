from brown.interface.font_interface import FontInterface
from brown.core import brown
from brown.core.font import Font
from brown.utils import smufl
from brown.utils.units import convert_all_to_unit


class MusicFontMetadataNotFoundError(Exception):
    """Exception raised when metadata for a music font can't be found."""
    pass


class MusicFont(Font):

    """A SMuFL compliant music font"""

    _interface_class = FontInterface

    def __init__(self, family_name, size, default_unit=None):
        super().__init__(family_name, size, 1, False)
        self.default_unit = default_unit
        self._cached_em_size = self._calculate_approximate_em_size()
        try:
            self.metadata = brown.registered_music_fonts[family_name]
            if self.default_unit:
                convert_all_to_unit(self.metadata, self.default_unit)
        except KeyError:
            raise MusicFontMetadataNotFoundError
        self._engraving_defaults = self.metadata['engravingDefaults']

    ######## PUBLIC PROPERTIES ########

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font."""
        return self._cached_em_size

    @property
    def engraving_defaults(self):
        """dict: The SMuFL engraving defaults information for this font"""
        return self._engraving_defaults

    ######## PRIVATE METHODS ########

    def _calculate_approximate_em_size(self):
        """Approximate the em size in the font.

        HACK: Because Qt doesn't make it clear how to find the true em height,
              we have to compute the em height by taking the height of a simple
              notehead (1/4 em unit) and multiply it by 4.

        Returns: GraphicUnit
        """
        return self._interface.tight_bounding_rect_around('\uE0A4').height * 4

    ######## PUBLIC METHODS ########

    def glyph_info(self, glyph_name):
        """Collect and return all known metadata about a glyph.

        Args:
            glyph_name (str): The canonical name of the glyph

        Returns:
            None: If the glyph name is not available in the font
            dict: A collection of all known metadata about the glyph
        """
        info = {}

        # Aggregate data from font-specific metadata
        try:
            info["glyphBBox"] = self.metadata['glyphBBoxes'][glyph_name]
        except KeyError:
            pass
        try:
            info['alternates'] = self.metadata[
                'glyphsWithAlternates'][glyph_name]['alternates']
        except KeyError:
            pass
        try:
            info['anchors'] = self.metadata['glyphsWithAnchors'][glyph_name]
        except KeyError:
            pass
        try:
            info['componentGlyphs'] = self.metadata['ligatures'][glyph_name]['componentGlyphs']
        except KeyError:
            pass
        for set_key in self.metadata['sets'].keys():
            for glyph in self.metadata['sets'][set_key]['glyphs']:
                if glyph['alternateFor'] == glyph_name:
                    info['setAlternatives'] = {}
                    info['setAlternatives'][set_key] = {}
                    info['setAlternatives'][set_key]['description'] = self.metadata['sets'][set_key]['description']
                    info['setAlternatives'][set_key]['name'] = glyph['name']
                    info['setAlternatives'][set_key]['codepoint'] = glyph['codepoint']
        info['is_optional'] = glyph_name in self.metadata['optionalGlyphs']
        # At this point if info is still empty, there is no metadata for the
        # glyph in the font, so we can assume this glyph doesn't exist.
        if not info:
            return None

        # Aggregate data from smufl spec

        info['codepoint'] = smufl.glyph_names[glyph_name]['codepoint']
        info['description'] = smufl.glyph_names[glyph_name]['description']
        info['classes'] = smufl.get_glyph_classes(glyph_name)
        return info
