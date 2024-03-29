from __future__ import annotations

from fractions import Fraction
from typing import Optional, Union, cast

from neoscore.utils.math_helpers import float_to_rounded_fraction_tuple


class Beat:
    """A beat in a meter whose value is measured in rational numbers.

    The beat fraction indicates beat as a fraction of a whole note.
    The actual written denomination of beat is deduced
    from the reduced fraction. For instance:

    * `Beat(1, 4)` indicates a quarter note value
    * `Beat(1, 1)` indicates a whole note value
    * `Beat(3, 8)` indicates a dotted quarter note value

    Arbitrarily nested tuplets can be created by nesting Beats
    in each other. To do this, let the numerator of a Beat
    be a Beat where the denominator indicates the division
    within the outer Beat. The actual written denomination
    of the durataion is inferred.

    * `Beat(Beat(1, 3), 4)` indicates an eighth in a triplet
      spanning a quarter
    * `Beat(Beat(1, 5), 8)` indicates a 32nd in a quintuplet
      spanning an eighth
    * `Beat(Beat(2, 10), 8)` is equivalent to
      `Beat(Beat(1, 5), 8)` seen above, for the same reason
      that `Beat(2, 8)` is equivalent to `Beat(1, 4)`
    * `Beat(Beat(3, 10), 8)` indicates a dotted 32nd in a quintuplet
      spanning an eighth.

    Nested Beats are not reduced into each other:
    * `Beat(Beat(1, 2), 4)` is *not* equivalent to `Beat(1, 8)`

    Beats should be treated as immutable, and will not work correctly
    if their properties are changed after initialization.

    # TODO LOW: How to handle things like duplet over dotted quarter?
    """

    def __init__(self, numerator: Union[int, Beat], denominator: int):
        self._numerator = numerator
        self._denominator = denominator
        self._collapsed_fraction = self.to_fraction()

        # Calculate base division and dot count
        if isinstance(self.numerator, type(self)):
            self._dot_count = self.numerator.dot_count
            # TODO LOW: This is wrong !!!
            # Beat(Beat(1, 3), 4) base division should be 8
            # for triplet eighth!
            self._base_division = self.denominator
            self._requires_tie = False
        else:
            dot_count = 0
            partial_numerator = self.collapsed_fraction.numerator
            partial_denominator = self.collapsed_fraction.denominator
            while partial_numerator > 1:
                partial_numerator = (partial_numerator - 1) / 2
                partial_denominator = partial_denominator / 2
                dot_count += 1
            if partial_numerator != 1:
                self._requires_tie = True
            else:
                self._requires_tie = False
            self._base_division = int(partial_denominator)
            self._dot_count = dot_count

    ######## CONSTRUCTORS ########

    @classmethod
    def from_float(
        cls, value: float, round_to: Optional[int] = None, limit_denominator: int = 1024
    ) -> Beat:
        """Initialize from a float with an optional denominator to round toward.

        Args:
            value:
            round_to: A denominator to round toward.
            limit_denominator: The maximum denominator value.
                If `round_to` is specified, this does nothing.

        Examples:
            >>> Beat.from_float(0.4)
            Beat(2, 5)
            >>> Beat.from_float(0.4, 2)
            Beat(1, 2)
            >>> Beat.from_float(0.4, 4)
            Beat(2, 4)
        """
        fraction_tuple = float_to_rounded_fraction_tuple(
            value, round_to, limit_denominator
        )
        return cls(*fraction_tuple)

    @classmethod
    def from_def(cls, beat_def: BeatDef) -> Beat:
        if isinstance(beat_def, Beat):
            return beat_def
        return Beat(*beat_def)

    ######## PUBLIC PROPERTIES ########

    @property
    def requires_tie(self) -> bool:
        """If this Beat requires a tie to be written."""
        return self._requires_tie

    @property
    def numerator(self) -> Union[int, Beat]:
        """The numerator component of the beat fraction.

        This may itself be a `Beat` if the outer beat represents a tuplet.
        """
        return self._numerator

    @property
    def denominator(self) -> int:
        """The denominator component of the beat fraction."""
        return self._denominator

    @property
    def dot_count(self) -> int:
        """The number of dots this beat has."""
        return self._dot_count

    @property
    def base_division(self) -> int:
        """The basic division of the beat."""
        # TODO LOW Explain more what this means
        return self._base_division

    @property
    def collapsed_fraction(self) -> Fraction:
        """Fraction: The collapsed `int / int` `Fraction` of this beat."""
        return self._collapsed_fraction

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return "{}({}, {})".format(
            type(self).__name__, self.numerator, self.denominator
        )

    def __hash__(self):
        """`Beat`s equal to each other share the same hash."""
        return 2387591 ^ hash(self.numerator) ^ hash(self.denominator)

    def __float__(self):
        """Reduce the fractional representation to a `float` and return it."""
        return float(self.collapsed_fraction)

    def __eq__(self, other):
        """Beats are equal if their numerators and denominators are."""
        if not isinstance(other, type(self)):
            return False
        return (
            self.numerator == other.numerator and self.denominator == other.denominator
        )

    def __add__(self, other):
        """Durations are added by adding their reduced fractions.

        Adding nested durations results in collapsing them into
        non-nested Durations
        """
        if not isinstance(other, type(self)):
            raise TypeError
        added_fraction = self.collapsed_fraction + other.collapsed_fraction
        return type(self)(added_fraction.numerator, added_fraction.denominator)

    def __sub__(self, other):
        """Durations are subtracted by subtracting their reduced fractions.

        Subtracting nested durations results in collapsing them into
        non-nested Durations
        """
        if not isinstance(other, type(self)):
            raise TypeError
        added_fraction = self.collapsed_fraction - other.collapsed_fraction
        return type(self)(added_fraction.numerator, added_fraction.denominator)

    def __gt__(self, other):
        """Beats are ordered by their reduced fraction representations."""
        if not isinstance(other, type(self)):
            return False
        return self.collapsed_fraction > other.collapsed_fraction

    def __ge__(self, other):
        """Beats are ordered by their reduced fraction representations.

        Because `Beat.__gt__` operates on the reduced fraction representation
        of the Beats being compared, but `Beat.__eq__` compares based on exact
        non-reduced matches, Beats may pass `Beat.__ge__`, but not
        `Beat.__eq__` if their numerators are nested differently. As such:

            >>> Beat(1, 4) >= Beat(Beat(1, 1), 4)
            True
            >>> Beat(1, 4) == Beat(Beat(1, 1), 4)
            False

        """
        return self > other or self.collapsed_fraction == other.collapsed_fraction

    def __lt__(self, other):
        """Beats are ordered by their reduced fraction representations."""
        if not isinstance(other, type(self)):
            return False
        return self.collapsed_fraction < other.collapsed_fraction

    def __le__(self, other):
        """Beats are ordered by their reduced fraction representations.

        Because `Beat.__lt__` operates on the reduced fraction representation
        of the Beats being compared, but `Beat.__eq__` compares based on exact
        non-reduced matches, Beats may pass `Beat.__le__`, but not
        `Beat.__eq__` if their numerators are nested differently. As such:

            >>> Beat(1, 4) <= Beat(Beat(1, 1), 4)
            True
            >>> Beat(1, 4) == Beat(Beat(1, 1), 4)
            False

        """
        return self < other or self.collapsed_fraction == other.collapsed_fraction

    ######## PUBLIC METHODS ########

    def to_fraction(self) -> Fraction:
        """Collapse this `Beat` into a single `Fraction` and return it.

        This recursively collapses any nested `Beat`s and simplifies
        the returned `Fraction`.

        Returns: Fraction
        """
        if isinstance(self.numerator, type(self)):
            return Fraction(self.numerator.collapsed_fraction, self.denominator)
        return Fraction(cast(int, self.numerator), self.denominator)


BeatDef = Union[Beat, tuple[int, int]]
"""A Beat or a shorthand tuple for one.

The tuple shorthand does not support nested beats; these should be created explicitly.
"""
