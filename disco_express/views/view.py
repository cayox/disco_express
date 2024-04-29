from PyQt6 import QtWidgets


class View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName(self.__class__.__name__)

        self._build_ui()

    def _build_ui(self):
        raise NotImplementedError
