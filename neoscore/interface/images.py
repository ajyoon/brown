from PyQt5.QtGui import QBitmap, QRegion

from neoscore.utils.units import Inch, Mm

supported_formats = {
    ".bmp",
    ".jpg",
    ".jpeg",
    ".png",
    ".pbm",
    ".pgm",
    ".ppm",
    ".xbm",
    ".xpm",
}

_inches_per_meter = Inch(1) / Mm(1000)


def dpi_to_dpm(dpi):
    """Convert a Dots Per Inch value to Dots Per Meter

    Args:
        dpi (int): A Dots Per Inch value

    Returns:
        int: A Dots Per Meter value
    """
    return dpi / _inches_per_meter


_QT_MASK_IN_COLOR = 0


def autocrop(q_image, q_color):
    """Automatically crop a qt image around the pixels not of a given color.

    Args:
        q_image (QImage):
        q_color (QColor):

    Returns:
        QImage: A newly cropped Qt image. The passed-in image is left
            unmodified.
    """

    mask = q_image.createMaskFromColor(q_color.rgb(), _QT_MASK_IN_COLOR)
    crop_rect = QRegion(QBitmap.fromImage(mask)).boundingRect()
    return q_image.copy(crop_rect)
