from brown.utils import color


def test_rgb_to_hex():
    assert(color.rgb_to_hex((0, 0, 0)) == '#000000')
    assert(color.rgb_to_hex((256, 256, 256)) == '#FFFFFF')
    assert(color.rgb_to_hex((184, 134, 11)) == '#B8860B')
