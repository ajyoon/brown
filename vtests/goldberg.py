import os
import sys

from neoscore.common import *

neoscore.setup()

expressive_font = Font("Lora", Mm(1.5), italic=True)

flowable = Flowable((Mm(0), Mm(0)), Mm(500), Mm(30), Mm(10))

upper_staff = Staff((Mm(0), Mm(0)), Mm(500), flowable, Mm(1))
lower_staff = Staff((Mm(0), Mm(12)), Mm(500), flowable, Mm(1))
Brace(Mm(0), {upper_staff, lower_staff})

# We can use the same unit in the upper and lower staves since they
# are the same size
unit = upper_staff.unit

upper_clef = Clef(upper_staff, unit(0), "treble")
lower_clef = Clef(lower_staff, unit(0), "bass")

# Once flowable gutters are implemented, this explicit offsets for
# key/time sigs will not be needed
KeySignature(upper_clef.bounding_rect.width + unit(0.5), upper_staff, "g_major")
KeySignature(lower_clef.bounding_rect.width + unit(0.5), lower_staff, "g_major")

TimeSignature(unit(5), Beat(3, 4), upper_staff)
TimeSignature(unit(5), Beat(3, 4), lower_staff)

Dynamic((unit(7), unit(6)), "p", upper_staff)
Text((unit(10), unit(6)), "dolce", expressive_font, upper_staff)

# Upper staff notes
Chordrest(unit(8), upper_staff, ["g''"], Beat(1, 4))
Chordrest(unit(12), upper_staff, ["g''"], Beat(1, 4))
a = Chordrest(unit(16), upper_staff, ["a''"], Beat(3, 16))
MusicText((unit(-1), unit(-2)), "ornamentMordent", a)
Chordrest(unit(19), upper_staff, ["b''"], Beat(1, 16))

# Lower staff notes - upper voice
Rest(Point(unit(10), unit(-3)), lower_staff, Beat(1, 4))
Chordrest(unit(16), lower_staff, ["d'"], Beat(1, 4), stem_direction=-1)

# Lower staff notes - middle voice
# Can't use Chordrest for these rests because Chordrest doesn't
# currently support explicit vertical positioning of rests.
Rest(Point(unit(8), unit(-2)), lower_staff, Beat(1, 4))
Chordrest(unit(12), lower_staff, ["b"], Beat(2, 4), stem_direction=-1)

# Lower staff notes - lower voice
Chordrest(unit(8), lower_staff, ["g"], Beat(3, 4))

BarLine(unit(22), [upper_staff, lower_staff])

if "--image" in sys.argv:
    image_path = os.path.join(os.path.dirname(__file__), "output", "goldberg.png")
    neoscore.render_image((Mm(0), Mm(0), Inch(2), Inch(2)), image_path, autocrop=True)
elif "--pdf" in sys.argv:
    # PDF export is currently broken
    pdf_path = os.path.join(os.path.dirname(__file__), "output", "goldberg.pdf")
    neoscore.render_pdf(pdf_path)
else:
    neoscore.show()
