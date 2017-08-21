class QEarleOverridden:
    """UI method overrides to be applied to all uses of QGraphicsItem classes.

    QGraphicsItem classes should generally not be used directly in `brown`.
    Instead, a subclass should be made from the Qt class with this class
    passed in a second superclass.

    In order for these overrides to have effect with python's MRO, ensure
    this class is listed after the Qt class in the class declaration.

    This class should never directly be instantiated.
    """

    def __init__(self, interface):
        """Do not call directly in subclasses.

        Instead, add `interface` as a kwarg to the Qt object constructor.

        This is due to some magic that PyQt performs for multiple inheritance
        with mixin classes.

        See http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html#cooperative-multi-inheritance
        """
        self._interface = interface

    def mousePressEvent(self, event):
        self._pos_before_move = self.scenePos()

    def mouseMoveEvent(self, event):
        delta = event.scenePos() - event.buttonDownScenePos(1)
        self.setPos(self._pos_before_move + delta)

    @property
    def interface(self):
        """Interface: The brown interface which owns this qt object."""
        return self._interface
