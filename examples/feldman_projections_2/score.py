from brown.core.music_char import MusicChar
from brown.core import brown
from examples.feldman_projections_2.register import Register as Reg
from examples.feldman_projections_2.grid_unit import GridUnit as G
from examples.feldman_projections_2.measure import Measure as M

fl = 'Flute'
tpt = 'Trumpet'
vln = 'Violin'
vc = 'Cello'
pnoL = 'PianoL'
pnoR = 'PianoR'


DIAMOND = MusicChar(brown.default_music_font, 'noteheadDiamondWhite')
SUB_2 = '\u2082'
P2 = 'P' + SUB_2


content = [
    # (instrument, pos_x, Register, text, length)
    (pnoL, M(0) + G(1), Reg.L, '5',     G(3) + M(1) + G(2)),
    (tpt,  M(0) + G(2), Reg.M, '',      G(3)),

    (pnoR, M(1),        Reg.M, '1',     G(1)),

    (tpt,  M(2),        Reg.L, '',      G(2)),
    (vln,  M(2) + G(1), Reg.H, DIAMOND, G(1)),
    (vc,   M(2) + G(2), Reg.M, P2,      G(1)),
    (pnoR, M(2) + G(2), Reg.L, '1',     G(1)),
    (fl,   M(2) + G(3), Reg.H, '',      G(1) + G(3)),
    (tpt,  M(2) + G(3), Reg.H, '',      G(1)),
    (pnoR, M(2) + G(3), Reg.H, '7',     G(1)),

    (vc,   M(3) + G(2), Reg.L, P2,      G(1)),
    (vln,  M(3) + G(3), Reg.M, 'A',     G(1) + G(1)),

    (pnoR, M(4) + G(1), Reg.L, '2',     G(1)),
    (vc,   M(4) + G(2), Reg.H, P2,      G(1)),

    (fl,   M(5),        Reg.M, '',      G(1)),
    (pnoL, M(5) + G(2), Reg.M, '1',     G(2) + G(3)),

    (vc,   M(6) + G(1), Reg.L, 'A',     G(1)),
    (vc,   M(6) + G(2), Reg.H, DIAMOND, G(1)),
    (fl,   M(6) + G(3), Reg.L, '',      G(1)),
    (tpt,  M(6) + G(3), Reg.H, '',      G(1)),
    (pnoR, M(6) + G(3), Reg.M, '3',     G(1)),

    (vc,   M(7) + G(3), Reg.M, P2,      G(1)),
    (vln,  M(7) + G(3), Reg.M, P2,      G(1)),

    (fl,   M(8) + G(3), Reg.L, '',      G(1) + G(2)),
    (tpt,  M(8) + G(3), Reg.L, '',      G(1) + G(2)),
    (vln,  M(8) + G(3), Reg.M, 'A',     G(1) + G(2)),
    (vc,   M(8) + G(3), Reg.M, 'A',     G(1) + G(2)),

    (vc,   M(9) + G(2), Reg.H, 'A',     G(1)),
    (pnoR, M(9) + G(3), Reg.L, '1',     G(1)),
]


