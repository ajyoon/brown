from PyQt5.QtCore import QSize, QMarginsF
from PyQt5.QtGui import QPageLayout, QPageSize

from brown.config import config
from brown.interface.qt_to_util import unit_to_qt_float


class PaperInterface(QPageLayout):

    def __init__(self, paper):
        """Initialize a QPageLayout from a Paper object

        Margins are in the given `paper` are ignored so that,
        when used for printing, this interface allows printing
        over the page margins.

        Args:
            paper (Paper):
        """
        # Scaling ratio for Qt point 72dpi -> config.PRINT_DPI
        ratio = 72 / config.PRINT_DPI
        QPageLayout.__init__(
            self,
            QPageSize(
                QSize(
                    unit_to_qt_float(paper.width) * ratio,
                    unit_to_qt_float(paper.height) * ratio,
                ),
            ),
            QPageLayout.Portrait,
            # Ignore margins - see class docstring
            QMarginsF(0, 0, 0, 0)
        )
