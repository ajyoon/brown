import os
from brown.utils.units import Mm


class InvalidConfigError(Exception):
    """Exception raised when a configuration is set to something invalid."""
    pass


######## Constants that really shouldn't be changed ########

BROWN_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, 'resources')

######## Defaults ##########################################

# Default colors
DEFAULT_PEN_COLOR = (0, 0, 0)
DEFAULT_BRUSH_COLOR = (0, 0, 0, 0)

# Default pen thickness
DEFAULT_PEN_THICKNESS = 0  # GraphicUnits

# Paper type
DEFAULT_PAPER_TYPE = 'A4'

# Text Font
DEFAULT_TEXT_FONT_NAME = 'Cormorant Garamond'
DEFAULT_TEXT_FONT_SIZE = 12  # GraphicUnits

# Music Glyph Font
DEFAULT_MUSIC_FONT_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'Bravura.otf')
DEFAULT_MUSIC_FONT_METADATA_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
DEFAULT_MUSIC_FONT_NAME = 'Bravura'

# Print PPI
PRINT_PPI = 300

# Staff Height
DEFAULT_STAFF_UNIT = Mm(1)
