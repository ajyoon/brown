from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface


class TextObjectInterface(GraphicObjectInterface):
    def __init__(self, x, y, text, font, parent=None):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
            parent: The parent interface object
        """
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsSimpleTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self.x = x
        self.y = y
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """float: The x position relative to the document."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._qt_object.setX(self._x)

    @property
    def y(self):
        """float: The y position relative to the document."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._qt_object.setY(self._y)

    @property
    def pen(self):
        """
        PenInterfaceQt: The pen to draw outlines with
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._pen:
            self._qt_object.setPen(self._pen._qt_object)
        else:
            # Use Qt default pen.
            # TODO: Make global default pen and use that instead
            self._qt_object.setPen(QtGui.QPen())

    @property
    def brush(self):
        """
        BrushInterfaceQt: The brush to draw outlines with
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._brush:
            self._qt_object.setBrush(self._brush._qt_object)
        else:
            # Use Qt default brush.
            # TODO: Make global default brush and use that instead
            self._qt_object.setBrush(QtGui.QBrush())

    @property
    def parent(self):
        """GraphicObjectInterface: The interface of the parent object."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            self._qt_object.setParentItem(value._qt_object)
        else:
            self._qt_object.setParentItem(None)

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        else:
            self._text = value

    @property
    def font(self):
        """ font (FontInterface): The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        # TODO: Propogate font change to qt object

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)