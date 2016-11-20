#!/usr/bin/env python3

import random

from brown.utils.mm import Mm
from brown.core import brown
from brown.core.font import Font
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.primitives.clef import Clef
from brown.primitives.staff import Staff
from brown.primitives.notehead import Notehead
from brown.primitives.chordrest import ChordRest
from brown.primitives.ledger_line import LedgerLine
from brown.core.flowable_frame import FlowableFrame

from brown.config import config


brown.setup()

glyph = Glyph((50, 100), '\uE118', brown.music_font)
glyph.render()

path = Path((0, 0), Pen('#f29000'), Brush('#eeeeee'))
path.line_to((100, 200), parent=glyph)
path.render()



brown.show()
