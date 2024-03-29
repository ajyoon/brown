from neoscore.core.path_element import CurveTo
from neoscore.utils.point import Point
from neoscore.utils.units import Unit


def assert_almost_equal(left, right, places=7):
    if isinstance(left, Unit):
        _assert_units_almost_equal(left, right, places)
    elif isinstance(left, Point):
        _assert_points_almost_equal(left, right, places)
    else:
        raise TypeError("Unsupported types")


def _assert_units_almost_equal(left, right, places):
    if round(left.base_value - right.base_value, places) != 0:
        left_type = type(left)
        right_type = type(right)
        raise AssertionError(
            "{} and {} not equal within {} Unit decimal places.\n"
            "Both as {}: {} vs {}\n"
            "Both as {}: {} vs {}".format(
                left,
                right,
                places,
                left_type.__name__,
                left,
                left_type(right),
                right_type.__name__,
                right_type(left),
                right,
            )
        )


def _assert_points_almost_equal(left, right, places):
    _assert_units_almost_equal(left.x, right.x, places)
    _assert_units_almost_equal(left.y, right.y, places)


def assert_path_els_equal(left, right):
    """Assert equality of the basic attributes of two PathElements

    This only checks position and parents, skipping their incidental
    attributes inherited from GraphicObject like `children`, `brush`,
    etc
    """
    assert type(left) == type(right)
    assert_almost_equal(left.pos, right.pos)
    assert left.parent == right.parent
    if isinstance(left, CurveTo):
        assert_path_els_equal(left.control_1, right.control_1)
        assert_path_els_equal(left.control_2, right.control_2)
