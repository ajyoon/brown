from neoscore.managed.instrument_family import InstrumentFamily
from neoscore.models.clef_type import ClefType


class Instrument:

    """Basic information on an instrument's notation conventions.

    This should be thought of as a basic enumeration of fixed
    information. To create a new instrument, subclass this
    and set its various class attributes.

    Notably, instruments are not meant to be actually instantiated.
    They have no __init__ method.
    """

    name = None
    """str: The full name of this instrument."""

    short_name = None
    """str: The shortened version of this instrument's name.

    This is the name that will typically appear on systems after the first one.
    For example, "Violoncello" might be shortened to "Vc."
    """

    staves = None
    """List[tuple(ClefType, Transposition)]: Default clefs and transpositions.

    This specifies the default properties of the staves this instrument
    typically uses. For most instruments, this will be a single staff.

    Each staff is given in a tuple of the form: `(ClefType, Transposition)`.
    To not use any `Transposition` set that value to `None`
    """

    family = None
    """InstrumentFamily: The general category of this instrument."""

    def __init__(self):
        raise TypeError("Instruments cannot be instantiated.")


class Flute(Instrument):
    name = "Flute"
    short_name = "Fl"
    staves = [(ClefType.TREBLE, None)]
    family = InstrumentFamily.WIND


class Trumpet(Instrument):
    """A trumpet written in sounding pitch"""

    name = "Trumpet"
    short_name = "Tpt"
    staves = [(ClefType.TREBLE, None)]
    family = InstrumentFamily.BRASS


class Piano(Instrument):
    """A two-staff piano"""

    name = "Piano"
    short_name = "Pno"
    staves = [(ClefType.TREBLE, None), (ClefType.BASS, None)]
    family = InstrumentFamily.KEYBOARD


class Violin(Instrument):
    """A general purpose violin"""

    name = "Violin"
    short_name = "Vln"
    staves = [(ClefType.TREBLE, None)]
    family = InstrumentFamily.STRING


class ViolinI(Violin):
    """A `Violin` with different naming for first violin."""

    name = "Violin I"
    short_name = "Vln I"


class ViolinII(Violin):
    """A `Violin` with different naming for second violin."""

    name = "Violin II"
    short_name = "Vln II"


class Viola(Instrument):
    """A general purpose viola."""

    name = "Viola"
    short_name = "Vla"
    staves = [(ClefType.ALTO, None)]
    family = InstrumentFamily.STRING


class Cello(Instrument):
    """A general purpose cello."""

    name = "Cello"
    short_name = "Vc"
    staves = [(ClefType.BASS, None)]
    family = InstrumentFamily.STRING


class Violoncello(Cello):
    """A general purpose cello, with its more traditional name."""

    name = "Violoncello"


class Bass(Instrument):
    """A general purpose bass."""

    name = "Bass"
    short_name = "Cb"
    staves = [(ClefType.BASS_8VB, None)]
    family = InstrumentFamily.STRING


class Contrabass(Bass):
    """A general purpose bass, with its more traditional name."""

    name = "Contrabass"
