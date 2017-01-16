"""Various interoperable units classes and some related helper functions."""


class Unit:
    """
    A fundamental base unit acting as a common ground for unit conversions.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (`+`, `-`, `/`, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from brown.utils.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.0393701)

    If a `Unit` (or subclass) is to the left of an `int` or `float`,
    the value on the right will be converted to the left object's type
    before performing the operation. The resulting value will be a new
    object of the left-side object's type.

        >>> print(Inch(1) + 1)
        Inch(2)

    If an `int` or `float` are on the left hand side of any operator
    except `*`, `/`, or `//`, a TypeError will be raised.

        >>> print(2 * Inch(1))
        Inch(2)
        >>> print(1 + Inch(1))
        Traceback (most recent call last):
         ...
        TypeError: unsupported operand type(s) for +: 'int' and 'Inch'
    """

    # Ratio of this class's units to Units.
    # Subclasses should override this.
    _base_units_per_self_unit = 1

    def __init__(self, value):
        """
        Args:
            value (int, float, Unit): The value of the unit.
                `int` and `float` literals will be stored directly
                into `self.value`. Any value which is a unit subclass of
                `Unit` will be converted to that value in this unit.
        """
        if isinstance(value, (int, float)):
            self.value = value
        elif type(value) == type(self):
            # Same type as self, just duplicate value
            self.value = value.value
        elif isinstance(value, Unit):
            # Convertible type, so convert value
            self.value = (value._to_base_unit_float()
                          / self._base_units_per_self_unit)
            if isinstance(self.value, float) and self.value.is_integer():
                self.value = int(self.value)
        else:
            raise TypeError(
                'Cannot create {} from {}'.format(type(self).__name__,
                                                  type(value).__name__))

    ######## PRIVATE METHODS ########

    def _to_base_unit_float(self):
        """Return this value as a float in base unit values.

        Returns: float
        """
        return self.value * self._base_units_per_self_unit

    ######## SPECIAL METHODS ########

    # Representations ---------------------------------------------------------

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.value)

    def __hash__(self):
        return hash(self.__repr__())

    # Comparisons -------------------------------------------------------------

    def __lt__(self, other):
        return self.value < type(self)(other).value

    def __le__(self, other):
        return self.value <= type(self)(other).value

    def __eq__(self, other):
        return self.value == type(self)(other).value

    def __gt__(self, other):
        return self.value > type(self)(other).value

    def __ge__(self, other):
        return self.value >= type(self)(other).value

    # Operators ---------------------------------------------------------------

    def __add__(self, other):
        return type(self)(self.value + type(self)(other).value)

    def __sub__(self, other):
        return type(self)(self.value - type(self)(other).value)

    def __mul__(self, other):
        return type(self)(self.value * type(self)(other).value)

    def __truediv__(self, other):
        return type(self)(self.value / type(self)(other).value)

    def __floordiv__(self, other):
        return type(self)(self.value // type(self)(other).value)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return type(self)(self.value ** type(self)(other).value)
        else:
            return type(self)(
                pow(self.value, type(self)(other).value, modulo))

    def __neg__(self):
        return type(self)(-self.value)

    def __pos__(self):
        return type(self)(+self.value)

    def __abs__(self):
        return type(self)(abs(self.value))

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __round__(self, ndigits=None):
        return type(self)(round(self.value, ndigits))

    # Reverse Operators -------------------------------------------------------

    def __rmul__(self, other):
        return type(self)(other * self.value)

    def __rtruediv__(self, other):
        return type(self)(other / self.value)

    def __rfloordiv__(self, other):
        return type(self)(other // self.value)


class GraphicUnit(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _base_units_per_self_unit = 1

    # (all other functionality implemented in Unit)
    pass


class Inch(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _base_units_per_self_unit = 300

    # (all other functionality implemented in Unit)
    pass


class Mm(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _base_units_per_self_unit = Inch._base_units_per_self_unit * 0.0393701

    # (all other functionality implemented in Unit)
    pass


class Cm(Unit):
    _base_units_per_self_unit = Mm._base_units_per_self_unit * 10

    # (all other functionality implemented in Unit)
    pass


def _call_on_immutable(iterable, unit):
    """Recursively convert all numbers in an immutable iterable.

    This is a helper function for convert_all_to_unit

    Args:
        iterable [tuple]: The iterable to recursive convert
        unit (type): The unit to convert numerical elements to

    Returns:
        An iterable the same type of the input.
        (set --> set, tuple --> tuple, etc.)
    """
    original_type = type(iterable)
    mutable_iterable = list(iterable)
    convert_all_to_unit(mutable_iterable, unit)
    return original_type(mutable_iterable)


def convert_all_to_unit(iterable, unit):
    """Recursively convert all numbers found in an iterable to a unit in place.

    This function works in place. Immutable structures (namely tuples) found
    within `iterable` will be replaced. `iterable` itself may not be immutable.

    In dictionaries, *only values* will be converted. Keys will be left as-is.

    Args:
        iterable [list, dict]: The iterable to recursive convert
        unit (type): The unit to convert numerical elements to

    Returns:
        None

    Raises:
        TypeError: If `iterable` is not an iterable or is immutable
    """
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if isinstance(value, (int, float, Unit)):
                iterable[key] = unit(value)
            elif isinstance(value, (list, dict)):
                convert_all_to_unit(iterable[key], unit)
            elif isinstance(value, (tuple, set)):
                iterable[key] = _call_on_immutable(iterable[key], unit)
            # (else: continue --- nothing to do here)
    elif isinstance(iterable, list):
        for i in range(len(iterable)):
            if isinstance(iterable[i], (int, float, Unit)):
                iterable[i] = unit(iterable[i])
            elif isinstance(iterable[i], (list, dict)):
                convert_all_to_unit(iterable[i], unit)
            elif isinstance(iterable[i], (tuple, set)):
                iterable[i] = _call_on_immutable(iterable[i], unit)
            # (else: continue --- nothing to do here)
    else:
        raise TypeError
