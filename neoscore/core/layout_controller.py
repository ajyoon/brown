from typing import cast

from neoscore.core.invisible_object import InvisibleObject
from neoscore.core.page import Page
from neoscore.utils.point import Point
from neoscore.utils.units import Unit

# TODO MEDIUM does it make sense for these to be InvisibleObjects?
# Does it make sense that LayoutControllers can have their parent
# changed?


class LayoutController(InvisibleObject):
    """An abstract layout controller for working with Flowable layouts."""

    def __init__(self, pos: Point, page: Page, flowable_x: Unit):
        """
        Args:
            pos: The position of this controller relative to its page.
            page: The page this controller appears on. This is used as
                the object's parent.
            flowable_x: The position of this controller within the owning
                flowable's local space.
        """
        super().__init__(pos, page)
        self._flowable_x = flowable_x

    ######## PUBLIC PROPERTIES ########

    @property
    def page(self) -> Page:
        """The page this controller appears on.

        This is identical to `self.parent`.
        """
        return cast(Page, self.parent)

    @property
    def flowable_x(self) -> Unit:
        """Unit: The x position in `self.flowable`s local space."""
        return self._flowable_x

    @flowable_x.setter
    def flowable_x(self, value: Unit):
        self._flowable_x = value
